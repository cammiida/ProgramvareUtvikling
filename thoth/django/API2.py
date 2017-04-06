# Importering av pakker for å kjøre scriptet. 
from projectoxford.luis import LuisClient   #   - Denne må lastes ned. Kjør: "pip install projectoxford" i et shell så tror jeg det skal være fikset. 
import sys, os, django, json
sys.path.append(os.path.join(os.path.dirname(__file__), 'thoth'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thoth.settings")
django.setup()
from django.conf import settings
#from google.cloud import language
import operator
from website.models import Question, Api

#=================================================================
# Adressen som refererer til applikasjonen jeg har lagd.
lc = LuisClient("https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/02aedc35-bf24-4785-99b9-a33f1d3ec9e5?subscription-key=23cfce88ff264c91bf16d76242b21f85&staging=true&timezoneOffset=0.0&verbose=true&q=")

#Synonymer til Action entiteten. bare å legge inn flere synonymer og andre actions man føler er nødvendige.
handling = {"bruke": ["use", "used", "using", "works", "apply", "work"], "lage": ["make", "create", "generate", "form", "cause", "produce", "prepare", "write"], "virke": ["work", "handle", "apply", "control", "manage", "operate"], "sortere":["sort", "arrange", "catalogue", "classify", "distribute"], "handle": ["do", "achieve", ]}

#Brukes til å teste. Ikke noe å bry seg om
#q = Question.objects.filter(question__startswith='how')

# Denne metoden finner entitetene i spørsmålet og lagrer dette i api-databasen. Denne har kun to viktige felt: entity_word og entity_type.
def predict(q):
    question = str(q)
    liste = {}
    ents = lc.query(question)
    for i in range(0, len(ents[2])):
        a = Api(entity_word=str(ents[1][i]), entity_type=str(ents[2][i]), question=q)
        a.save()
        
# Denne metoden henter ut entiteter allerede lagt inn i databasen. Den vil kun hente ut entiteter som allerede har et svar tilknyttet seg. Dette sjekker den ved å se på answer_set. Denne attributten blir satt når læreren svarer på et spørsmål 
def fetch(typ, word):
    query = Api.objects.all().filter(entity_type__exact=typ, entity_word__exact=word).exclude(answer_set=False)
    return query

# Dette er hovedmetoden. Her skjer sammenligningen av spørsmålet som nettopp ble stilt og alle spørsmålene i databasen som har svar. Det meste blir kommentert der det trengst. Også et par kommentarer som brukes av meg for å vite hva jeg har igjen å gjøre.    
def similar(q):
    question = str(q)
    liste = {}
    likt_sporsmal = {}
    navn = ""
    ents = lc.query(question)
    for i in range(0, len(ents[2])):
        
        if(ents[2][i] == "QuestionWord" and ents[1][i] == "what"):
            ls2 = fetch(ents[2][i], "how")
            print(ls)
            ls = fetch(ents[2][i], ents[1][i])
            liste[str(ents[2][i])] = []
            for l in ls:
                liste[str(ents[2][i])].append(str(l))
            for l in ls2:
                liste[str(ents[2][i])].append(str(l))
            continue
                
        if(ents[2][i] == "Action"):                         #   - Gjør det slik at man kan bruke synonymene jeg har lagret i handlingsdictionarien for actions 
            for name, age in handling.items():              #   - Dette gjør at man ikke trenger å bruke nøyaktig de samme ordene, men programmet finner uanseett
                if(str(ents[1][i]) in str(age)):            #   - hva du mente med spørsmålet basert på synonyer av ordet du brukte. Disse må stå i handlingslisten
                    navn = name
                    print(navn)
            liste[str(ents[2][i])] = []
            for n in handling[navn]:
                ls = fetch(ents[2][i], n)
                print(ls)
                for l in ls:
                    liste[str(ents[2][i])].append(str(l))
        else:
            ls = fetch(ents[2][i], ents[1][i])
            liste[str(ents[2][i])] = []
            for l in ls:
                liste[str(ents[2][i])].append(str(l))
            
#  Dette kjører hvis det ikke er en action. Vil da ikke gå inn i handlingsdictionarien og kjøre synonymer. Alt annet vil derfor ikke sjekke om synonymer av ordene enda. 
    for d in liste:
        print(d)
        print(liste[d])
        print("\n")
        
                                                                # - Skal brukes senere til å sjekke opp hvilke spørreord som kan brukes om hverandre (som synonymer)
    try:                                                        # - Må ha denne for å sjekke om det faktisk finnes en algoritme i spørsmålet. Hvis ikke må den kjøre en alternativ rute.
        for alg in liste['Algorithm']:
            if(alg in liste['QuestionWord'][0]):                # - Antar her at det kun er et spørreord i hver setning. Velger at hvis et spørsmål handler om en algoritme så må den                                                             algoritmen bli nevnt i det like spørsmålet. 
                likt_sporsmal[alg] = 1                          # - Spørreord og algoritme er her like
                try:
                    if(alg in liste['ProgrammingLanguages']):   #   - Kan videre teste om programmeringsspråket som brukes i setningen er lik. Hvis det finnes spørsmål som har lik
                        likt_sporsmal[alg] += 1                 #     algoritme, men ingen programmeringsspråk i spørsmålet må disse også være med videre ettersom generelle svar kan hjelpe.
                        print("kommer den hit?")                     
                                                                # - Fant ut at det var et likt programmeringsspråk i spørsmålet.
                except:
                    print("Her var det ingenting!")             # - Altså ingen programmeringsspråk i spørsmålet og derfor ikke vits å sjekke videre på. 
                                                                # - Skal her hente ut svaret fra dette spørsmålet og gi det tilbake til brukeren (Eller fortsette å teste videre...)
                print("kjører denne?")
                try:
                    if(alg in str(liste['Action'])):
                        likt_sporsmal[alg] += 1
                except:
                    print("fantes ingen action å ta av!")

                # Dette finner det spørsmålet som har flest like elementer og setter dette som svaret fra API. 
                hoyeste = max(likt_sporsmal.items(), key=operator.itemgetter(1))[0]    
                query = Question.objects.get(question=hoyeste)
                print(query)
                q.api_answer = str(query.answer)
                q.save()            
                                                            #   - Ting å utvide med senere:
                                                            #   - Teste om objektene som brukes i spørsmålet er like. Om de er like kan være vanskelig å sjekke, men kan lage en liste av       synonymer, men starter uten.
                                                            #   - Adjektiver er også noe som kan testes. Vanskelige er synonymer her også. Lister kan virke som beste måte å gå frem her. Vil   ikke hjelpe for alle tilfeller, men tror ikke det er nødvendig på dette nivået. 
                                                            #   - Må legge til hva som skjer hvis det er flere spørsmål som er like nok til å gi ut svar!
    except:
        for question in liste['QuestionWord']:
            try:
                if(question in liste['Action']):
                    likt_sporsmal[question] = 1
                    try:
                        if(question in liste['Objects']):
                            likt_sporsmal[question] += 1
                    except:
                        continue
            except:
                print("var ingen actions i setningen!")
            

# Dette brukes til testing så ingenting å bry seg om.
   
#print(q[2])
#similar("How to sort a list of objects?")
#predict(q[3])
#predict(q[0])
#predict(q[2])
#print(fetch("Algorithm", "merge sort"))
#for i in range(0,len(d[2])):
 #   if(d[2][i] == "Algorithm"):
  #      pass
   # if(d[2][i] == "Action"):
    #    pass
    #if(d[2][i] == "ProgrammingLanguage"):
     #   pass
    #if(d[2][i] == "QuestionWord"):
     #   pass












# Tingene i databasene er kun ting som kan være nyttig å bruke senere og som jeg kun har tatt med for å kunne utvide med. Gjør det også lettere for meg å vite hva jeg trenger å huske på med tanke på setningsoppbygning. 

#===============    Databaser   ========================
#   - Dette er de tradisjonelle spørreordene som brukes. Her er noen veldig generelle, mens andre stiller spesifikke spørsmål om feks personer eller tid. 
sprOrd = ["where", "how", "who", "when", "which", "why", "What"]

#   - Kan spørre videre hvis jeg får vite at spørreordet er How om hva som er neste ord etter det. Dette gir en dypere spesialisering av spørsmål
how = ["how much", "how many", "how often", "how far", "how to", "how do"]



#klassifisering av spørreord:
#Who - bare til personer. Hvis dette ordet er i en setning kan jeg anta at det skal være en person i spørsmålet
#Where - Handler om plassering. Hvis det kommer en algoritme i dette spørsmålet må det handle om hvor i algoritmen noe skal skje.
#How - Hvordan noe skjer. Er et vidt spørsmål. Hvis det kommer en algoritme i dette spørsmålet må man ha en action(noe til å spesifisere hva det spørres om)
#When - Handler for det meste om tid, men kan handle om når noe kommer i forhold til spørsmål. Algoritme kan komme her.
#Which - Også ganske vidt spørsmål. Gjør det enklere med en spesifisering av spørsmål. 
#Why - Handler om hvorfor noe skjer eller brukes. Hvorfor spørsmål kan være alene. 
#What - Spør om spesifikk informasjon. Må da være en spesifisering i spørsmålet et sted. Algoritme eller andre entiteter. 


#   - Må finne like handlinger som kan brukes i samme setning uten å ekskludere hverandre slik at hvis man har det ene kan man få det andre.

#   - Dette er også måter å starte spørsmål på, men er ikke de tradisjonelle ordene man bruker og krever mer logikk for å få til. 
andre = ["is there", "is it", "could you"]
