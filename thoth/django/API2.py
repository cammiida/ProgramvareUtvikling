from projectoxford.luis import LuisClient
import sys, os, django, json
sys.path.append(os.path.join(os.path.dirname(__file__), 'thoth'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thoth.settings")
django.setup()
from django.conf import settings
from google.cloud import language
import operator
from website.models import Question, Api


#=================================================================
lc = LuisClient("https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/02aedc35-bf24-4785-99b9-a33f1d3ec9e5?subscription-key=23cfce88ff264c91bf16d76242b21f85&timezoneOffset=0.0&verbose=true&q=")

handling = {"bruke": ["use", "used", "using", "works", "apply"], "lage": ["make", "create", "generate", "form", "cause", "produce", "prepare"], "virke": ["work", "handle", "apply", "control", "manage", "operate"], "sortere":["sort", "arrange", "catalogue", "classify", "distribute"], "handle": ["do", "achieve", ]}

q = Question.objects.filter(question__startswith='how')
#print(q[0])
#if(q[0].answer):
#    print("her var det et svar")
print(q[2])

def predict(q):
    question = str(q)
    liste = {}
    ents = lc.query(question)
    for i in range(0, len(ents[2])):
        a = Api(entity_word=str(ents[1][i]), entity_type=str(ents[2][i]), question=q)
        a.save()
    
def fetch(typ, word):
    query = Api.objects.all().filter(entity_type__exact=typ, entity_word__exact=word).exclude(answer_set=False)
    return query
    
#print(fetch("QuestionWord", "how")[0].answer)
    
def similar(q):
    question = str(q)
    liste = {}
    likt_sporsmal = {}
    navn = ""
    ents = lc.query(question)
    for i in range(0, len(ents[2])):
        
   
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
        
    sprWord = ents[1][ents[2].index("QuestionWord")]            # - Skal brukes senere til å sjekke opp hvilke spørreord som kan brukes om hverandre (som synonymer)
    try:                                                        # - Må ha denne for å sjekke om det faktisk finnes en algoritme i spørsmålet. Hvis ikke må den kjøre en alternativ rute.
        for alg in liste['Algorithm']:
            if(alg in liste['QuestionWord'][0]):                # - Antar her at det kun er et spørreord i hver setning. Velger at hvis et spørsmål handler om en algoritme så må den                                                             algoritmen bli nevnt i det like spørsmålet. 
                likt_sporsmal[alg] = 1                        # - Spørreord og algoritme er her like
                try:
                    if(alg in liste['ProgrammingLanguages']):   #   - Kan videre teste om programmeringsspråket som brukes i setningen er lik. Hvis det finnes spørsmål som har lik
                        likt_sporsmal[alg] += 1              #     algoritme,    
                        print("kommer den hit?")                #     men ingen programmeringsspråk i spørsmålet må disse også være med videre ettersom generelle svar kan hjelpe.
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
    
                hoyeste = max(likt_sporsmal.items(), key=operator.itemgetter(1))[0]    
                query = Question.objects.get(question=hoyeste)
                print(query)
                q.api_answer = str(query.answer)
                q.save() 
                                                            #   - Teste om objektene som brukes i spørsmålet er like. Om de er like kan være vanskelig å sjekke, men kan lage en liste av synonymer, men starter uten.
                                                            #   - Adjektiver er også noe som kan testes. Vanskelige er synonymer her også. Lister kan virke som beste måte å gå frem her. Vil ikke hjelpe for alle tilfeller, men tror ikke det er nødvendig på dette nivået. 
                                                            #   - Må legge til hva som skjer hvis det er flere spørsmål som er like nok til å gi ut svar!
    except:
        print("finnes ingen algoritme i spørsmålet!")
        

    
#print(q[2])
#similar(q[2])
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

like = ['']