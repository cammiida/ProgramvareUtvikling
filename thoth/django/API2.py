#=====================================================================
#                       NATURAL LANGUAGE API
#=====================================================================

# This API is a bit hard to understand. If you have any questions regarding the code or the LUIS application that is being used in this script please ask Håkon. I have tried to comment as well as I can, but the thoughts behind is perhaps not always clear. 

# Importing packages needed to run the script
# The projectOxford package have to be downloaded. Run "pip install projectoxford" to download this package from microsoft.
from projectoxford.luis import LuisClient   
import sys, os, django, json
sys.path.append(os.path.join(os.path.dirname(__file__), 'thoth'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thoth.settings")
django.setup()
from django.conf import settings
#from google.cloud import language - This was the google cloud API. Could be used to add further functionality to the script
import operator
from website.models import Question, Api
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

#=================================================================
# This is the address refering to the application I have made. When updating the application this address needs to be updated. 
lc = LuisClient("https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/02aedc35-bf24-4785-99b9-a33f1d3ec9e5?subscription-key=23cfce88ff264c91bf16d76242b21f85&staging=true&timezoneOffset=0.0&verbose=true&q=")

# This is used as a synonyms array to the Action entity. It is possible to add synonyms to expand functionality. 
handling = {"bruke": ["use", "used", "using", "works", "apply", "work"], "lage": ["make", "create", "generate", "form", "cause", "produce", "prepare", "write"], "virke": ["work", "handle", "apply", "control", "manage", "operate"], "sortere":["sort", "arrange", "catalogue", "classify", "distribute"], "handle": ["do", "achieve", ]}

# Used for testing.
#q = Question.objects.filter(question__startswith='What')

# This method finds the entities in the question. The entities are saved in the api database. It has only two important fields. entitiy_word and entity_type. 
def predict(q):
    question = str(q)
    liste = {}
    ents = lc.query(question)
    for i in range(0, len(ents[2])):
        a = Api(entity_word=str(ents[1][i]), entity_type=str(ents[2][i]), question=q)
        a.save()
        
# This method fetches the entities all ready in the database. It only fetches the entities that has an answer connected to it. It does this by checking the answer_set. This attribute is set when a teacher answers a question. 
def fetch(typ, word):
    query = Api.objects.all().filter(entity_type__exact=typ, entity_word__exact=word).exclude(answer_set=False)
    return query

# This is the main method of this script. It compares the question that was asked to all the answered questions in the database. Most of the difficult code is commentet bellow. 
def similar(q):
    # This is to make sure the question asked is in string form. 
    question = str(q)
    # Here are som dictionarys that will save information about the newly asked question and the questions already in the database. 
    liste = {}
    likt_sporsmal = {}
    navn = ""
    # This is the call to the LUIS application. This returns a kind of json object (kinda like a dictionay) with entities. Both the type and the word it recognized as this type. 
    ents = lc.query(question)
    #print(ents)
    # This for-loop goes through all the entities recognized.
    for i in range(0, len(ents[2])):
        # The sentence always have to contain a question word. A list of question words are added in the code at the bottom of this script. 
        # This if sentence is just a check to see if the questionword used is "what". This is because there are diffrent types of the same question that could use different question word. I have not added functionality for all the similar question word. Only if the question word is "What", then how is used as a synonym for this question word, when comparing.
        if(ents[2][i] == "QuestionWord" and ents[1][i] == "what"):
            # This is a call to the fetch function. It fetches all the questions that has a entitiy_word "how" in the sentence. This is the synonyms part to "what"
            ls2 = fetch(ents[2][i], "how")
            # This is a call to the fetch function with "what" as a parameter. Fetches all the questions with entitiy_word = "what"
            ls = fetch(ents[2][i], ents[1][i])
            # Here I use the liste dictionary to add an empty array on the form {"what": []}. This empty array is going to contain every question that has the entitiy_word = "what" or "how". 
            liste[str(ents[2][i])] = []
            # For-loops to loop through every fetched question. 
            for l in ls:
                liste[str(ents[2][i])].append(str(l))
            for l in ls2:
                liste[str(ents[2][i])].append(str(l))
            continue
            
        # Same functionality as the code above, but without the use of synonyms. Only the fetches questions with the exact question word used is.
        elif(ents[2][i] == "QuestionWord"):
            ls = fetch(ents[2][i], ents[1][i])
            liste[str(ents[2][i])] = []
            for l in ls:
                liste[str(ents[2][i]).append(str(l))]
         
        # Also same functionality as above, but this uses the synonym array handling to loop through a list of synonyms to the action used in the newly asked question.       
        if(ents[2][i] == "Action"):         
            # This checks if the action entity used in the question has synonyms in the "handling" array above. If it does it loops through all of the synonyms, fetching answered questions from the database that contains the synonyms. It is therefore not needed to use the exact same words when asking a question to trigger a similar question. 
            for name, age in handling.items():            
                if(str(ents[1][i]) in str(age)):            #   - hva du mente med spørsmålet basert på synonyer av ordet du brukte. Disse må stå i handlingslisten
                    navn = name
                    print(navn)
            # Same functionality as above. Just appending questions to the liste array on the form: {"action": [question, question, ...]}
            liste[str(ents[2][i])] = []
            for n in handling[navn]:
                ls = fetch(ents[2][i], n)
                for l in ls:
                    liste[str(ents[2][i])].append(str(l))
                    
        # Every entitiy that isn't a questionWord or an action should just check if there is a question that contains this entitiy_word. If there is such a question is is added in the liste array like this: {entitiy_type: [question, ...]}
        else:
            ls = fetch(ents[2][i], ents[1][i])
            liste[str(ents[2][i])] = []
            for l in ls:
                liste[str(ents[2][i])].append(str(l))    
    
    
#  Dette kjører hvis det ikke er en action. Vil da ikke gå inn i handlingsdictionarien og kjøre synonymer. Alt annet vil derfor ikke sjekke om synonymer av ordene enda. 
    print(liste)
    # Now I am done fetching questions. All the similar questions based on entities are now in the liste array. Here I am starting to compare the based on different requirements. This first try-sentence checks if there is an entitiy_type: algorithm in the newly asked question. If there is it will see if there is any answered questions in the database that contains this algorithm.
    try: 
        # If there is an algorithm it checks if an answered question that contains this algorithm also has the same questionWord some where in the question. It loops through every answered question that contains the algorithm in the newly asked question.                                                        
        for alg in liste['Algorithm']:
            # This is where the comparing is happening between questions containing the algorithm and questions containing the question Word used in the newly asked question. 
            if(alg in liste['QuestionWord'][0]):
                # If the compare is true this question is added to the likt_sporsmal dictionary on the form {question: INT}. If a newly asked question has some similarty with an asnwered question from the database the database question gets an incremented score. This score is stored in the likt_spormal dictionary with the question string as key. 
                likt_sporsmal[alg] = 1
                # This checks if the newly asked question contains a programming language like python. 
                try:
                    if(alg in liste['ProgrammingLanguages']):
                        # If there is an answered question in the database is similar with the newly asked question regarding both the questionWord, algorithm and programming lanugage it gets another point. 
                        likt_sporsmal[alg] += 1                              
                
                # This except tells us just that there wasn't any programming lanugage in the newly asked question. 
                except:
                    pass   
                    
                # Checks to see if there is a spesification::verb entitiy that is the same. A spesification::verb entitiy is the word that is following the question word like so: "What is a fish?". Here the spesification::verb is "is". 
                try:
                    if(alg in liste['Spesification::Verb']):
                        # There is a spesification::verd entitiy in the question and therefore it gets a point.
                        likt_sporsmal[alg] += 1    
                        
                # No spesification::verd entitiy in newly asked question.
                except:
                    pass
      
                try:
                    if(alg in str(liste['Action'])):
                        likt_sporsmal[alg] += 1
                except:
                    continue

                # Here I find the question with the most points in the likt_sporsmal dictionary. The string variable hoyeste then contains the string question. (the key) that has the highest score.
                hoyeste = max(likt_sporsmal.items(), key=operator.itemgetter(1))[0]   
                # If this score is above 0 it should save the answer to the answered question from the database as the API answer to the newly asked question. We have then found a question that is similar in crucial parts of the question so it is safe to say they could also have the same answer. 
                if(likt_sporsmal[hoyeste] > 0): 
                    query = Question.objects.exclude(answer="").get(question=hoyeste)
                    q.api_answer = str(query.answer)
                    q.save()                                
                                                            # A list in norwegian of features or improvements to add in the future.
                                                            #   - Ting å utvide med senere:
                                                            #   - Teste om objektene som brukes i spørsmålet er like. Om de er like kan være vanskelig å sjekke, men kan lage en liste av synonymer, men starter uten.
                                                            #   - Adjektiver er også noe som kan testes. Vanskelige er synonymer her også. Lister kan virke som beste måte å gå frem her. Vil   ikke hjelpe for alle tilfeller, men tror ikke det er nødvendig på dette nivået. 
                                                            #   - Må legge til hva som skjer hvis det er flere spørsmål som er like nok til å gi ut svar!
                                                            
    # This exception tells me that there is no algorithm in the newly asked question. The process below is the exact same as the one above, but I am comparing the questions based on different criterias. Here I am saying that a question has to have the same question word to be the same question. This is a bit narrow, and should be improved, but is in our simple meaning enough to build further on. 
    except:
        for question in liste['QuestionWord']:
            likt_sporsmal[question] = 0
            try:
                if(question in liste['objects']):
                    try:
                        if(question in liste['Action']):
                            likt_sporsmal[question] += 2
                            if(question in liste['Spesification::Verb']):
                                likt_sporsmal[question] += 1
            
                    except:
                        if(question in liste['Spesification::Verb']):
                            likt_sporsmal[question] += 2
                                            
            except:
                pass
        # exact same code as above. 
        hoyeste = max(likt_sporsmal.items(), key=operator.itemgetter(1))[0]  
        print(likt_sporsmal)
        if(likt_sporsmal[hoyeste] > 0):  
            query = Question.objects.exclude(answer="").get(question=hoyeste)
            q.api_answer = str(query.answer)
            q.save()



# This function updates the API answer (AKA the answer to a question so similar to a question the teacher have answered that it is safe to say it could have the same answer) to reflect when the teacher updates the original answer. 
def update(sprs, svar):
        q = Question.objects.get(question=sprs).answer
        spr = Question.objects.filter(api_answer=q)
        for p in spr:
            p.api_answer = svar
            p.save()

# 
#@receiver(post_save, sender=Question)
#def update2(sender, **kwargs):
 #   for q in spr:
  #      print(q)
    
    

# Used for testing purposes   
#print(q[1])
#predict(q[1])






# Tingene i databasene er kun ting som kan være nyttig å bruke senere og som jeg kun har tatt med for å kunne utvide med. Gjør det også lettere for meg å vite hva jeg trenger å huske på med tanke på setningsoppbygning. 

#===============    Databases   ========================

# This is a list of different question words I am counting the most normally used.  
sprOrd = ["where", "how", "who", "when", "which", "why", "What"]

#   - Kan spørre videre hvis jeg får vite at spørreordet er How om hva som er neste ord etter det. Dette gir en dypere spesialisering av spørsmål
# These are different types of the question word how. 
how = ["how much", "how many", "how often", "how far", "how to", "how do"]


# The comments below is for the developers that would try to improve this script. It is my own thoughs on how the question words is used and how they could help categorize what should come after (what types of entities the question could contain). Perhaps mostly for my own process of thinking. It is written in norwegian. 

#klassifisering av spørreord: 
#Who - bare til personer. Hvis dette ordet er i en setning kan jeg anta at det skal være en person i spørsmålet
#Where - Handler om plassering. Hvis det kommer en algoritme i dette spørsmålet må det handle om hvor i algoritmen noe skal skje.
#How - Hvordan noe skjer. Er et vidt spørsmål. Hvis det kommer en algoritme i dette spørsmålet må man ha en action(noe til å spesifisere hva det spørres om)
#When - Handler for det meste om tid, men kan handle om når noe kommer i forhold til spørsmål. Algoritme kan komme her.
#Which - Også ganske vidt spørsmål. Gjør det enklere med en spesifisering av spørsmål. 
#Why - Handler om hvorfor noe skjer eller brukes. Hvorfor spørsmål kan være alene. 
#What - Spør om spesifikk informasjon. Må da være en spesifisering i spørsmålet et sted. Algoritme eller andre entiteter. 



#   This is also a list of different ways to begin a question. 
andre = ["is there", "is it", "could you"]
