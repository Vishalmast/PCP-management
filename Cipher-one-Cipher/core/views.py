from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse, HttpResponse
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse

import pickle
from geopy.geocoders import ArcGIS
from geopy import distance
import geopy, pandas as pd
from .models import *
from sklearn.neural_network import MLPClassifier
from django_pandas.io import read_frame
qs = Patient.objects.all()

symptom, disease = [], []
disease_list = ['Fungal infection', 'Hepatitis B', 'Gastroenteritis', 'Allergy', 'Hepatitis E', 'Hypoglycemia', 'hepatitis A', 
'Pneumonia', 'GERD', 'Hypothyroidism', 'Jaundice', 'Hyperthyroidism', 'Chronic cholestasis', 'Heart attack', 'Hepatitis C', 
'Chicken pox', 'Varicose veins', 'Malaria', 'Dengue', 'Paralysis (brain hemorrhage)', 'Peptic ulcer diseae', 'Acne', 
'(vertigo) Paroymsal  Positional Vertigo', 'Hypertension ', 'Dimorphic hemmorhoids(piles)', 'Osteoarthristis', 'Alcoholic hepatitis', 
'AIDS', 'Hepatitis D', 'Tuberculosis', 'Urinary tract infection', 'Common Cold', 'Typhoid', 'Psoriasis', 'Drug Reaction', 'Diabetes ', 
'Bronchial Asthma', 'Cervical spondylosis', 'Impetigo', 'Migraine', 'Arthritis']

symptoms_list = [' joint_pain', ' sunken_eyes', ' weight_loss', ' cramps', ' indigestion', ' weight_gain', ' fast_heart_rate', ' red_sore_around_nose', ' unsteadiness', ' skin_peeling', ' lack_of_concentration', ' runny_nose', ' mild_fever', ' burning_micturition', ' ulcers_on_tongue', ' rusty_sputum', ' swollen_blood_vessels', ' loss_of_appetite', ' extra_marital_contacts', ' family_history', ' receiving_unsterile_injections', ' excessive_hunger', ' hip_joint_pain', ' receiving_blood_transfusion', ' neck_pain', ' painful_walking', ' history_of_alcohol_consumption', ' nausea', ' dark_urine', ' bruising', ' cold_hands_and_feets', ' stiff_neck', ' itching', ' pain_during_bowel_movements', ' weakness_in_limbs', ' palpitations', ' skin_rash', ' shivering', ' malaise', ' inflammatory_nails', ' loss_of_balance', ' high_fever', ' prominent_veins_on_calf', ' red_spots_over_body', ' obesity', ' movement_stiffness', ' fluid_overload', ' swelling_joints', ' silver_like_dusting', ' anxiety', ' puffy_face_and_eyes', ' mood_swings', ' scurring', ' drying_and_tingling_lips', ' distention_of_abdomen', ' congestion', ' restlessness', ' mucoid_sputum', ' back_pain', ' altered_sensorium', ' patches_in_throat', ' irregular_sugar_level', ' passage_of_gases', ' depression', ' irritability', ' polyuria', ' swollen_legs', ' weakness_of_one_body_side', ' loss_of_smell', ' breathlessness', ' bloody_stool', ' blister', ' stomach_bleeding', ' pain_behind_the_eyes', ' belly_pain', ' swollen_extremeties', ' diarrhoea', ' slurred_speech', ' continuous_feel_of_urine', ' dizziness', ' chills', ' muscle_pain', ' abdominal_pain', ' visual_disturbances', ' acute_liver_failure', ' vomiting', 'skin_rash', ' internal_itching', ' fatigue', ' swelling_of_stomach', ' yellowing_of_eyes', ' lethargy', ' yellow_urine', ' pain_in_anal_region', ' watering_from_eyes', ' throat_irritation', ' sinus_pressure', ' sweating', ' blackheads', ' acidity', ' spinning_movements', ' coma', ' blurred_and_distorted_vision', ' headache', ' dehydration', ' knee_pain', ' constipation', ' toxic_look_(typhos)', ' phlegm', ' blood_in_sputum', ' yellow_crust_ooze', ' continuous_sneezing', ' pus_filled_pimples', ' redness_of_eyes', ' nodal_skin_eruptions', ' swelled_lymph_nodes', ' brittle_nails', ' chest_pain', ' foul_smell_of urine', ' stomach_pain', ' muscle_weakness', ' bladder_discomfort', ' dischromic_patches', ' spotting_urination', ' irritation_in_anus', ' enlarged_thyroid', ' small_dents_in_nails', ' increased_appetite', ' muscle_wasting', ' cough', ' yellowish_skin', ' abnormal_menstruation']

disease_specialist_mapping = {'Migraine': 'Neurologists',
'Tuberculosis': 'Pulmonologists',
'Acne': 'Dermatologists',
'Hyperthyroidism': 'Endocrinologists',
'hepatitis A': 'Gastroenterologists',
'Malaria': 'Allergists',
'Typhoid': 'Allergists',
'Hypothyroidism': 'Endocrinologists',
'Peptic ulcer diseae': 'Gastroenterologists',
'Allergy': 'Dermatologists',
'Heart attack': 'Cardiac surgeons',
'Varicose veins': 'Neurologists',
'Gastroenteritis': 'Gastroenterologists',
'Diabetes ': 'Endocrinologists',
'Psoriasis': 'Dermatologists',
'AIDS': 'Allergists',
'Jaundice': 'Physician',
'GERD': 'Gastroenterologists',
'Osteoarthristis': 'Orthopedic surgeons',
'Pneumonia': 'Allergists',
'Bronchial Asthma': 'Pulmonologists',
'Alcoholic hepatitis': 'Gastroenterologists',
'(vertigo) Paroymsal  Positional Vertigo': 'Neurologists',
'Impetigo': 'Dermatologists',
'Drug Reaction': 'Allergists',
'Hypoglycemia': 'Physician',
'Hepatitis E': 'Gastroenterologists',
'Hepatitis B': 'Gastroenterologists',
'Cervical spondylosis': 'Orthopedic surgeons',
'Fungal infection': 'Dermatologists',
'Hepatitis D': 'Gastroenterologists',
'Urinary tract infection': 'Endocrinologists',
'Hepatitis C': 'Gastroenterologists',
'Chronic cholestasis': 'Gastroenterologists',
'Chicken pox': 'Allergists',
'Dengue': 'Allergists',
'Hypertension ': 'Cardiac surgeons',
'Dimorphic hemmorhoids(piles)': 'Physician',
'Paralysis (brain hemorrhage)': 'Neurologists',
'Common Cold': 'Physician',
'Arthritis': 'Orthopedic surgeons'}

#patients = pd.DataFrame({"UID": ['123456','234567'], "Name": ["Utkarsh", "Vignesh"], "Age": [25,26], "Street" : ["6011 W OUTER DR", "4001 TIETON DR"],
#"City" : ["Detroit","YAKIMA"], "State" : ["MI","WA"], "PIN" : [12345,345678], "Diss" : [[1598971327],[]]})

patients = read_frame(qs)

def lists(request):
    symptoms = symptoms_list
    diseases = disease_list 

    return render(request, 'add_listing.html', {'symptoms': symptoms, 'diseases':diseases})

def addInfo(request):
    global UID,name, age, street, city, pin, search_result, df
    UID = request.POST.get("UID")
    #This is to use for database to check if exist or not
    df = patients.loc[patients['UID'] == UID]
    print(df)
    if(df.empty == False):
        name = list(df["Name"])[0]
        #age = df["Age"][0]
        street = list(df["Street"])[0]
        city = list(df["City"])[0]
        state = list(df["State"])[0]
        pin = list(df["Pin"])[0]
        diss = list(df["Disatisfy"])[0]
    else:
        return render(request, 'not_register.html')
    print(name, street)
    symptom = request.POST.getlist("cb1")
    disease = request.POST.getlist("cb2")
    print(name, symptom, disease)
    "enter your Function here"
    specialist_list=['Dermatologists', 'Gastroenterologists', 'Physician', 'Allergists', 'Endocrinologists', 'Cardiac surgeons', 
    'Neurologists', 'Orthopedic surgeons', 'Pulmonologists']
    specialist=''
    if len(symptom)==0:
        d={}
        for a in disease:
            try:
                d[disease_specialist_mapping[a]]+=1
            except:
                d[disease_specialist_mapping[a]]=1   
        max_count=0
        for key in d.keys():
            if d[key]>max_count:
                specialist=key
                max_count=d[key]
    else:
        import pickle
        model = pickle.load(open("core\model.pkl", 'rb'))
        for i in range(len(symptom)):
            l=symptom[i].split()
            symptom[i]='_'.join(l)
            symptom[i]=' '+symptom[i]
        input_test=[]
        for i in symptoms_list:
            if i in symptom:
                print(i)
                input_test.append(1)
            else:
                input_test.append(0)
        input_test=[input_test]
        predict=model.predict(input_test)
        print(disease_list[predict[0]])
        print(disease_specialist_mapping[disease_list[predict[0]]])
        specialist=disease_specialist_mapping[disease_list[predict[0]]]
    doc_database=pd.read_csv('core\doctor_database_geocoded_final.csv')
    from geopy.geocoders import ArcGIS
    nom = ArcGIS()
    location=nom.geocode(street+' '+city+' '+state+' US')
    user_lat=location.latitude
    user_lon=location.longitude
    print(user_lat,user_lon)
    print(location.address)
    doc_subset=doc_database[doc_database['Provider Type of the Provider']==specialist]
    from geopy import distance

    for i in doc_subset.index:
        doc_subset.loc[i,'distance']=distance.distance((doc_subset.loc[i,'Latitude'],doc_subset.loc[i,'Longitude']),(user_lat,user_lon)).km
    doc_subset['score']=doc_subset['distance']-doc_subset['ratings']*2
    search_result = doc_subset.sort_values('score')[['National Provider Identifier','First Name of the Provider','Last Name/Organization Name of the Provider','Provider Type of the Provider','Address','distance','ratings']]
    search_result = search_result.rename(columns = {'National Provider Identifier': 'NPI','First Name of the Provider': 'First_name','Last Name/Organization Name of the Provider': 'Last_name', 'Provider Type of the Provider': 'Type'})
    search_result = search_result.head(50)
    NPIs = search_result["NPI"].tolist()
    """for i in search_result["NPI"]:
        if i in diss:
            search_result = search_result.drop(search_result[search_result["NPI"]==i].index, inplace=True)
"""
    search_result = search_result.round({"distance":2,"ratings":2})
    #print(type(search_result))
    #print(search_result)
    
    return render(request, "listing.html", {'dataframe':search_result.head(20), 'name':name, 'street':street, 'city':city, 'state':state, 'uid':UID})

def dissatisfy(request):
    global search_result
    #npi = request.POST.get("npi")
    #print(npi)
    #search_result = search_result.drop(search_result[search_result["NPI"]==npi].index, inplace=True)
    #return HttpResponse("Hello")
    return render(request, "listing.html", {'dataframe':search_result})

def profile(request):
    UID = request.GET.get("UI")
    print(UID)
    df = patients.loc[patients['UID'] == UID]
    
    if(df.empty):
        return render(request, 'not_register.html')
    if(list(df['Current'])[0]==0):
        doc = pd.DataFrame()
    else:
        doc = pd.read_csv('core\doctor_database_geocoded_final.csv')
        doc = doc.loc[doc['National Provider Identifier'] == df['Current'][0]]
        doc = doc.rename(columns = {'National Provider Identifier': 'NPI','First Name of the Provider': 'First_name','Last Name/Organization Name of the Provider': 'Last_name', 'Provider Type of the Provider': 'Type'})
    npi = str(doc.NPI).split()[1]
    f_name = str(doc.First_name).split()[1]
    l_name = str(doc.Last_name).split()[1]
    type = str(doc.Type).split()[1]
    print(npi, f_name, l_name, type)
    return render(request, "profile.html", {'data': df, 'npi': npi, 'f_name': f_name, 'l_name': l_name, 'type': type})

def book(request):
    global UID
    uid = UID
    # uid = request.POST.get('uid')
    NPI = request.POST.get('npi')
    print(NPI)
    t = Patient.objects.get(UID=uid)
    t.Current = NPI
    t.save()

    df = patients.loc[patients['UID'] == UID]
    df['Current'][0] = NPI
    doc = pd.read_csv('core\doctor_database_geocoded_final.csv')
    doc = doc.loc[doc['National Provider Identifier'] == df['Current'][0]]
    doc = doc.rename(columns = {'National Provider Identifier': 'NPI', 'First Name of the Provider': 'First_name','Last Name/Organization Name of the Provider': 'Last_name', 'Provider Type of the Provider': 'Type'})
    npi = str(doc.NPI).split()[1]
    f_name =  str(doc.First_name).split()[1]
    l_name = str(doc.Last_name).split()[1]
    type = str(doc.Type).split()[1]
    print(npi, f_name, l_name, type)
    return render(request, "profile.html", {'data': df, 'npi': npi, 'f_name': f_name, 'l_name': l_name, 'type': type})

def address(request):
    UID = request.POST.get('UID')
    street = request.POST.get('street')
    city = request.POST.get('city')
    state = request.POST.get('state')
    pin = request.POST.get('pin')
    return render(request, "profile.html", {'data':df, 'doctor':doc})

def addview(request):

    return render(request, "address.html")

class HomeView(ListView):
    template_name = 'listing.html'
    queryset = Patients.objects.filter(flagged=False)
    context_object_name = 'listings'
    paginate_by = 30







