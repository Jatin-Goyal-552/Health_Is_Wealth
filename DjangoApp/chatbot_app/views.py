from django.urls import reverse
from .models import *
from django.shortcuts import render, HttpResponse
import pickle
import random
import numpy as np
import pandas as pd
import random

disease_model= pickle.load(open('..//Disease_Prediction_Files//Multinomial_classifier_disease.pkl','rb'))
disease_tokenizer = pickle.load(open('..//Disease_Prediction_Files//tf_idf_vectorizer_disease.pkl','rb'))
df_description = pd.read_csv("..//Disease_Prediction_Files//DiseaseData//symptom_Description.csv")
df_precautions = pd.read_csv("..//Disease_Prediction_Files//DiseaseData//symptom_precaution.csv")
df_symptoms = pd.read_csv("..//Disease_Prediction_Files//DiseaseData//dataset.csv")
df_description['Disease'] = df_description['Disease'].apply(lambda x : x.lower())
df_precautions['Disease'] = df_precautions['Disease'].apply(lambda x : x.lower())
df_symptoms['Disease'] = df_symptoms['Disease'].apply(lambda x : x.lower())

print("---------------------You are set to go.--------------------------")


def clean(text):
    text = text.lower() 
    text = text.split()
    text = ' '.join(text)
    return text


def chatbot(request):
    global df_precautions, df_symptoms
    if request.method == 'POST':
        symptom1 = request.POST['Symptom 1']
        symptom2 = request.POST['Symptom 2']
        symptom3 = request.POST['Symptom 3']
        symptom4 = request.POST['Symptom 4']
        symptom5 = request.POST['Symptom 5']
        symptom6 = request.POST['Symptom 6']
        symptom7 = request.POST['Symptom 7']
        symptom8 = request.POST['Symptom 8']
        symptom9 = request.POST['Symptom 9']
        symptom10 = request.POST['Symptom 10']
        symptom11 = request.POST['Symptom 11']
        symptom12 = request.POST['Symptom 12']
        

        symptoms = symptom1 + " " + symptom2+ " " + symptom3+ " " + symptom4+ " " + symptom5+ " " + symptom6+ " " + symptom7+ " "+ symptom8+ " "  + symptom9+ " " + symptom10+ " " + symptom11+ " " + symptom12
        test=clean(symptoms)
        
        test=[test]
        test_vectorized=disease_tokenizer.transform(test)
        print(test_vectorized)
        pred=disease_model.predict(test_vectorized)[0]
        
        # Description of the disease
        disease = pred.lower()
        all_disease=df_description['Disease'].values.tolist()
        print(all_disease)
        find_disease=False
        if disease not in all_disease:
            description = "Sorry, I do not know description of this disease."
        else:
            description=str(df_description[df_description['Disease']==disease]['Description'].values[0])
        
        # Precaution of disease 
        df_precautions=df_precautions.fillna('')
        all_disease=df_precautions['Disease'].values.tolist()
        if  disease not in all_disease:
            precautions="Sorry, I do not know precaution of this disease."
        else:
            final_disease = disease
            precautions=str(df_precautions[df_precautions['Disease']==final_disease]['Precaution_1'].values[0]+", "+df_precautions[df_precautions['Disease']==final_disease]['Precaution_2'].values[0]+", "+df_precautions[df_precautions['Disease']==final_disease]['Precaution_3'].values[0]+" and  "+df_precautions[df_precautions['Disease']== final_disease]['Precaution_4'].values[0])
            precautions="You should take precaution like "+precautions+ "."
            
        # Symptoms of disease
        df_symptoms=df_symptoms.fillna('')
        all_disease = df_symptoms['Disease'].values.tolist()
        if disease not in all_disease:
            symptoms = "Sorry, I do not know symptoms of this disease."
        else:
            df_symptoms2=df_symptoms[df_symptoms['Disease']==disease].reset_index() 
            temp_symptoms_list = []  # List to store symptoms of the disease
            for i in range(0, df_symptoms2.shape[0]):
                for j in range(1,18):
                    col='Symptom_'+str(j)
                    if df_symptoms2.iloc[i][col] != "":
                        temp_symptom = " ".join(df_symptoms2.iloc[i][col].split("_"))
                        if temp_symptom not in temp_symptoms_list:
                            temp_symptoms_list.append(temp_symptom)
                    
                                    
            all_symptoms = ", ".join(temp_symptoms_list[:-1])
            all_symptoms += " " + "and " + temp_symptoms_list[-1]
                        
            symptoms="Symptoms for this disease is "+ all_symptoms + "."
            print(symptoms)
        context = {
            "disease": pred,
            "description":description,
            "precautions":precautions,
            "symptoms":symptoms
        }
        return render(request, "disease_result.html", context)
    
    return render(request,'all_disease.html')


