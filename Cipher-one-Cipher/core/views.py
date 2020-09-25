from django.shortcuts import render


import datetime
from datetime import date
from plotly.graph_objs import Bar
from plotly.graph_objs import Heatmap
from plotly.graph_objs import Bar, Scatter
import json
import plotly
from django.db.models import F

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
df_patient_data = read_frame(Patient.objects.all())
df_upcoming_patients = read_frame(Upcoming_patient.objects.all())


def schedule(request):
    UID = request.GET.get('UID', '')
    schedule_date = request.GET.get('scheduletime', '')

    qs = Patient.objects.all()
    patients = read_frame(qs)
    df = patients.loc[patients['UID'] == UID]

    if (df.empty):
        return render(request, 'not_register.html')
    if (list(df['Current'])[0] == 0):
        doc = pd.DataFrame()
    else:
        doc = pd.read_csv('core\doctor_database_geocoded_final.csv')
        doc = doc.loc[doc['National Provider Identifier'] == list(df['Current'])[0]]
        doc = doc.rename(columns={'National Provider Identifier': 'NPI', 'First Name of the Provider': 'First_name',
                                  'Last Name/Organization Name of the Provider': 'Last_name',
                                  'Provider Type of the Provider': 'Type', 'Fees': 'fee'})
    npi = str(doc.NPI).split()[1]
    f_name = str(doc.First_name).split()[1]
    l_name = str(doc.Last_name).split()[1]
    type = str(doc.Type).split()[1]
    bill = float(str(doc.fee).split()[1])

    # qs = Patient.objects.filter(UID=F("UID"))
    # print(qs)
    print(df)
    print(df.iloc[0, 11])
    deductible = df.iloc[0, 11]
    deductible_paid = df.iloc[0, 12]
    copay = df.iloc[0, 9]
    coinsurance = df.iloc[0, 10]
    limit = df.iloc[0, 7]
    left = df.iloc[0, 8]

    def compute_payment(bill, deductible, deductible_paid, copay, coinsurance, limit, left):
        bill_left = bill
        payment_by_dependant = 0
        payment_by_payor = 0
        if deductible_paid < deductible:
            payment_by_dependant = min(deductible - deductible_paid, bill)
            deductible_paid += payment_by_dependant
            left -= payment_by_dependant
            bill_left -= payment_by_dependant
        if bill_left > copay and left > copay:
            payment_by_dependant += min(left, copay + (bill_left - copay) * 0.2)
            left -= min(left, copay + (bill_left - copay) * 0.2)
            payment_by_payor = bill - payment_by_dependant
        elif bill_left <= copay and left > copay:
            payment_by_dependant += bill_left
            left -= bill_left
            payment_by_payor = bill - payment_by_dependant
        else:
            payment_by_dependant += left
            left = 0
            payment_by_payor = bill - payment_by_dependant
        return payment_by_dependant, payment_by_payor, deductible_paid, left

    payment_by_dependant, payment_by_payor, deductible_paid, left = compute_payment(bill, deductible, deductible_paid, copay, coinsurance, limit, left)
    t = Patient.objects.get(UID=UID)
    t.Deduct_Paid = deductible_paid
    t.Limit_left = left
    t.save()

    t = Upcoming_patient.objects
    t.create(UID = UID, Scheduled_date = schedule_date, Payment_by_payer = payment_by_payor, Payment_by_dependant=payment_by_dependant)

    pname = df.iloc[0, 1]
    state = df.iloc[0, 4]
    street = df.iloc[0, 2]
    city = df.iloc[0, 3]

    return render(request, "profile.html",
                  {'UID': UID, 'pname': pname, 'street': street, 'city': city, 'state': state, 'npi': npi,
                   'f_name': f_name, 'l_name': l_name, 'type': type})
    # return render(request, "profile.html")


def ins(request):
    def patients_list_for_provider(ins_plan):
        li = []
        for i in range(df_patient_data.shape[0]):
            if df_patient_data.loc[i, 'Insurance_policy_plan'] == ins_plan:
                li.append(df_patient_data.loc[i, 'UID'])
        return li

    def upcoming_charges(patient_li, days_to_track=7):
        today = datetime.date.today()
        li = [0 for i in range(days_to_track)]
        li2 = [0 for i in range(days_to_track)]
        li_date = []
        for i in range(days_to_track):
            li_date.append(today)
            today += datetime.timedelta(days=1)

        for ind, date in enumerate(li_date):
            for i in range(df_upcoming_patients.shape[0]):
                if df_upcoming_patients.loc[i, 'Scheduled_date'] == date and df_upcoming_patients.loc[i, 'UID'] in patient_li:
                    li[ind] += df_upcoming_patients.loc[i, 'Payment_by_payer']
                    li2[ind] += df_upcoming_patients.loc[i, 'Payment_by_dependant']
        return li, li_date, li2

    li_a, li_date, li2_a = upcoming_charges(patients_list_for_provider('a'))
    li_b, li_date, li2_b = upcoming_charges(patients_list_for_provider('b'))
    li_c, li_date, li2_c = upcoming_charges(patients_list_for_provider('c'))
    for i in range(len(li_a)):
        li_a[i] = li_a[i] + li_b[i] + li_c[i]
    for i in range(len(li_a)):
        li2_a[i] = li2_a[i] + li2_b[i] + li2_c[i]
    li = li_a
    li2 = li2_a
    graphs = [
        {
            'data': [
                Bar(
                    x=li_date,
                    y=li
                )
            ],

            'layout': {
                'title': 'Distribution of upcoming charges',
                'yaxis': {
                    'title': "Charge"
                },
                'xaxis': {
                    'title': "Date"
                }
            }
        },
        {
            'data': [
                Bar(
                    x=li_date,
                    y=li2
                )
            ],

            'layout': {
                'title': 'Distribution of upcoming charges for dependent',
                'yaxis': {
                    'title': "Charge"
                },
                'xaxis': {
                    'title': "Date"
                }
            }
        }
    ]

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render(request, 'insaurance_page.html', {'ids': ids, 'graphJSON': graphJSON})


def go(request):
    # save user input in query
    query = request.GET.get('query', '')
    def patients_list_for_provider(ins_plan):
        li = []
        for i in range(df_patient_data.shape[0]):
            if df_patient_data.loc[i, 'Insurance_policy_plan'] == ins_plan:
                li.append(df_patient_data.loc[i, 'UID'])
        return li

    def upcoming_charges(patient_li, days_to_track=7):
        today = datetime.date.today()
        li = [0 for i in range(days_to_track)]
        li2 = [0 for i in range(days_to_track)]
        li_date = []
        for i in range(days_to_track):
            li_date.append(today)
            today += datetime.timedelta(days=1)

        for ind, date in enumerate(li_date):
            for i in range(df_upcoming_patients.shape[0]):
                if df_upcoming_patients.loc[i, 'Scheduled_date'] == date and df_upcoming_patients.loc[i, 'UID'] in patient_li:
                    li[ind] += df_upcoming_patients.loc[i, 'Payment_by_payer']
                    li2[ind] += df_upcoming_patients.loc[i, 'Payment_by_dependant']
        return li, li_date, li2

    li, li_date, li2 = upcoming_charges(patients_list_for_provider(query))

    graphs = [
        {
            'data': [
                Bar(
                    x=li_date,
                    y=li
                )
            ],

            'layout': {
                'title': 'Distribution of upcoming charges',
                'yaxis': {
                    'title': "Charge"
                },
                'xaxis': {
                    'title': "Date"
                }
            }
        },
        {
            'data': [
                Bar(
                    x=li_date,
                    y=li2
                )
            ],

            'layout': {
                'title': 'Distribution of upcoming charges for dependent',
                'yaxis': {
                    'title': "Charge"
                },
                'xaxis': {
                    'title': "Date"
                }
            }
        }]

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # This will render the go.html Please see that file.
    return render(
        request,
        'insaurance_extended.html',

        {'query': query, 'classification_result': None, 'ids': ids, 'graphJSON': graphJSON}
    )
def lists(request):
    symptoms = symptoms_list
    diseases = disease_list 

    return render(request, 'add_listing.html', {'symptoms': symptoms, 'diseases':diseases})

def addInfo(request):
    qs = Patient.objects.all()
    patients = read_frame(qs)
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
    qs = Patient.objects.all()
    patients = read_frame(qs)
    qs_2 = Upcoming_patient.objects.all()
    upcoming_patients = read_frame(qs_2)
    UID = request.GET.get("UI")
    print(UID)
    df = patients.loc[patients['UID'] == UID]
    df2 = upcoming_patients.loc[upcoming_patients['UID'] == UID]
    flag = 1
    booking_date = None
    if df2.empty:
        flag = 0
    else:
        booking_date = df2.iloc[0, 1]
    if(df.empty):
        return render(request, 'not_register.html')
    else:
        pname = list(df['Name'])[0]
        street = list(df['Street'])[0]
        city = list(df['City'])[0]
        state = list(df['State'])[0]
    if(list(df['Current'])[0]==0):
        doc = pd.DataFrame()
    else:
        doc = pd.read_csv('core\doctor_database_geocoded_final.csv')
        doc = doc.loc[doc['National Provider Identifier'] == list(df['Current'])[0]]
        doc = doc.rename(columns = {'National Provider Identifier': 'NPI','First Name of the Provider': 'First_name','Last Name/Organization Name of the Provider': 'Last_name', 'Provider Type of the Provider': 'Type'})
    npi = str(doc.NPI).split()[1]
    f_name = str(doc.First_name).split()[1]
    l_name = str(doc.Last_name).split()[1]
    type = str(doc.Type).split()[1]
    print(npi, f_name, l_name, type)

    return render(request, "profile.html", {'flag': flag, 'booking_date':booking_date,'UID': UID, 'pname': pname, 'street': street, 'city': city, 'state': state, 'npi': npi, 'f_name': f_name, 'l_name': l_name, 'type': type})


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
    qs = Patient.objects.all()
    patients = read_frame(qs)
    UID = request.POST.get('UID')
    street = request.POST.get('street')
    city = request.POST.get('city')
    state = request.POST.get('state')
    pin = request.POST.get('pin')
    t = Patient.objects.get(UID=UID)
    name = t.Name
    t.Street = street
    t.City = city
    t.State = state
    t.Pin = pin
    cur = t.Current
    t.save()
    # print(UID)
    # df = patients.loc[patients['UID'] == UID]
    # df['Current'][0] = NPI
    # doc = pd.read_csv('core\doctor_database_geocoded_final.csv')
    # doc = doc.loc[doc['National Provider Identifier'] == df['Current'][0]]
    # doc = doc.rename(columns={'National Provider Identifier': 'NPI', 'First Name of the Provider': 'First_name',
    #                           'Last Name/Organization Name of the Provider': 'Last_name',
    #                           'Provider Type of the Provider': 'Type'})
    # npi = str(doc.NPI).split()[1]
    # f_name = str(doc.First_name).split()[1]
    # l_name = str(doc.Last_name).split()[1]
    # type = str(doc.Type).split()[1]
    # print(npi, f_name, l_name, type)
    # return render(request, "profile.html", {'data': df, 'npi': npi, 'f_name': f_name, 'l_name': l_name, 'type': type})
    # # return render(request, "profile.html", {'data':df, 'doctor':doc})
    doc = pd.read_csv('core\doctor_database_geocoded_final.csv')
    doc = doc.loc[doc['National Provider Identifier'] == cur]
    doc = doc.rename(columns={'Provider Type of the Provider': 'Type'})
    type = str(doc.Type).split()[1]
    specialist = type
    print(specialist)
    doc_database = pd.read_csv('core\doctor_database_geocoded_final.csv')
    from geopy.geocoders import ArcGIS
    nom = ArcGIS()
    location = nom.geocode(street + ' ' + city + ' ' + state + ' US')
    user_lat = location.latitude
    user_lon = location.longitude
    print(user_lat, user_lon)
    print(location.address)
    doc_subset = doc_database[doc_database['Provider Type of the Provider'] == specialist]
    from geopy import distance

    for i in doc_subset.index:
        doc_subset.loc[i, 'distance'] = distance.distance(
            (doc_subset.loc[i, 'Latitude'], doc_subset.loc[i, 'Longitude']), (user_lat, user_lon)).km
    doc_subset['score'] = doc_subset['distance'] - doc_subset['ratings'] * 2
    search_result = doc_subset.sort_values('score')[
        ['National Provider Identifier', 'First Name of the Provider', 'Last Name/Organization Name of the Provider',
         'Provider Type of the Provider', 'Address', 'distance', 'ratings']]
    search_result = search_result.rename(
        columns={'National Provider Identifier': 'NPI', 'First Name of the Provider': 'First_name',
                 'Last Name/Organization Name of the Provider': 'Last_name', 'Provider Type of the Provider': 'Type'})
    search_result = search_result.head(50)
    NPIs = search_result["NPI"].tolist()

    search_result = search_result.round({"distance": 2, "ratings": 2})


    return render(request, "listing.html",
                  {'dataframe': search_result.head(20), 'name': name, 'street': street, 'city': city, 'state': state,
                   'uid': UID})


def addview(request):

    return render(request, "address.html")

class HomeView(ListView):
    template_name = 'listing.html'
    queryset = Patients.objects.filter(flagged=False)
    context_object_name = 'listings'
    paginate_by = 30







