from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.shortcuts import render, HttpResponse
import pickle
import json
import random
import numpy as np
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
import keras
import random
from .forms import corona_xray_form
from textblob import TextBlob
import keras
import cv2
from collections import Counter
import os
from time import sleep
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from keras.preprocessing.image import ImageDataGenerator,load_img, img_to_array


model = keras.models.load_model('..//Corona_Chatbot_Files//chatbot_model4.h5')
intents = json.loads(open('..//Corona_Chatbot_Files//intents.json').read())
words = pickle.load(open('..//Corona_Chatbot_Files//words.pkl','rb'))
classes = pickle.load(open('..//Corona_Chatbot_Files//classes.pkl','rb'))
print("---------------------You are set to go.--------------------------")


        
def chatbot(request):
    return render(request,'chatbot.html')

def clean(text):
    text = text.lower() 
    text = text.split()
    text = ' '.join(text)
    return text

def clean_up_sentence(sentence):
    ignore_words=['covid','corona','covid-19','19','breastfeed','newborn','unborn','viruses','viruse','varient']

    lemmatizer = WordNetLemmatizer()
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words2=[]
    for a in sentence_words:
        if a.lower() not in ignore_words:
            sentence_words2.append(str(TextBlob(a).correct()))
        else:
            sentence_words2.append(a)
    sentence_words=sentence_words2 
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words,show_details=True)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result,tag

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res,tag = getResponse(ints, intents)
    return res,tag

def home(request):
    if request.method == 'POST':
        print("---------------------------------")
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        print(send_mail(subject, email +" :- "+message,settings.EMAIL_HOST_USER, ["goyaljatin310@gmail.com"], fail_silently=False))
        return render(request,'home.html')
    return render(request,'home.html')

def chatbot(request):
    return render(request,'corona_chatbot.html')

def predict_chat(request):
    pred="please type something"
    tag=""
    global prec,desc,sym,flag,temp_disease,all_symptoms
    if request.method == 'POST':
        print('hello')
        chat=request.POST['operation']
        pred,tag=chatbot_response(chat)
        # pred,tag=chatbot_response(chat)
    return HttpResponse(json.dumps({'ans':pred}), content_type="application/json")

def xray(request):
    form=corona_xray_form()
    
    if request.method == 'POST':
        form=corona_xray_form(request.POST,request.FILES)
        if form.is_valid():
            
            form.save()
        else:
            print(form.errors)
        # url=str(form.image)
        url=str(form.cleaned_data["image"])
        print("url",url)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sleep(5)
        image_location=os.path.join("media",url)
        model=keras.models.load_model("C://Users//LENOVO//projects//TRI Nit Hackathon//notebook//corona_model.h5")
        img = load_img(image_location, grayscale=False, target_size=(150, 150,3))
        img = img_to_array(img)
        img= img.reshape(1, 150, 150, 3)
        img = img.astype('float32')
        img = img / 255.0
        
        pred=model.predict(img)[0][0]
        print("pred",pred)
        if pred>0.5:
            prediction="This X-ray is Covid Negative."
        else:
            prediction="This X-ray is Covid Positive."
        corona = corona_xray.objects.all()
        sorted_xray= corona_xray.objects.order_by('corona_id').reverse()
        print("*****************************") 
        print("sorted",sorted_xray[0].corona_id)
        print("nnnnn")
        last=sorted_xray[0].corona_id
        xray=corona.filter(corona_id=last)
        print("mri",xray)
        return render(request, 'corona_xray_result.html',{"prediction": prediction,"xray":xray})
    return render(request,'corona_Xray_form.html',{"form": form})