import numpy as np
import nltk
import string
import random

f = open('chatbot.txt','r',errors = 'ignore')
raw_data = f.read()
raw_data = raw_data.lower()
nltk.download('punkt')
nltk.download('wordnet')
sentence = nltk.sent_tokenize(raw_data)
word = nltk.word_tokenize(raw_data)

lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
  return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct),None) for punct in string.punctuation)
def LemNormalize(text):
  return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

greet_inputs = ("hello","hi","greetings","sup","what's up","hey","hola","knock knock")
greet_responses = ["hi :)","hey :)","hiya :)","Howdy :)","hi there :)","hello :)","helloooo :)"]
def greet(senten):
  for w in senten.split():
    if w.lower() in greet_inputs:
      return random.choice(greet_responses)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def response(user_response):
  robo1_response = ''
  TfidVec = TfidfVectorizer(tokenizer = LemNormalize,stop_words ='english')
  tfidf = TfidVec.fit_transform(sentence)
  vals = cosine_similarity(tfidf[-1],tfidf)
  idx = vals.argsort()[0][-2]
  flat = vals.flatten()
  flat.sort()
  req_tfidf = flat[-2]
  if(req_tfidf == 0):
    robo1_response = robo1_response +"I am sorry :( I don't understand you"
    return robo1_response
  else:
    robo1_response = robo1_response +sentence[idx]
    return robo1_response

flag = True
print("cookmate : My name is cookmate.Type the ingredients you have ill suggest you the recipe name ,if you want to exit just type see ya!")
while(flag == True):
  print("user:",end = "")
  user_response = input()
  user_response = user_response.lower()
  if (user_response != "see ya"):
    if(user_response == "thanks" or user_response == "thank you"):
      flag = False
      print("cookmate : You are Welcome! :)")
    else:
      if(greet(user_response) != None):
        print("cookmate : "+greet(user_response))
      else:
        sentence.append(user_response)
        word = word + nltk.word_tokenize(user_response)
        final_words = list(set(word))
        print("cookmate : ",end = "")
        print(response(user_response))
        sentence .remove(user_response)
  else:
    flag = False
    print("cookmate : Bye! :) Have fun <3")
