from multiprocessing import AuthenticationError
from ssl import AlertDescription
from telnetlib import AUTHENTICATION
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from datetime import date
from django.urls import reverse_lazy, reverse
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from datetime import datetime, time
from time import sleep


from django.contrib.auth.models import User, auth
from transliterate import get_available_language_packs
from .models import patient, doctor, diseaseinfo, consultation, rating_review, consultingpayment, reportupload
from chats.models import Chat, Feedback
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import *
from .forms import *
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main_app.forms import ContactusForm
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib.auth import authenticate, login, logout
from datetime import datetime

from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q


# Create your views here.


# loading trained_model
import joblib as jb
model = jb.load('trained_svmmodel')


def home(request):

    if request.method == 'GET':

        if request.user.is_authenticated:
            return render(request, 'homepage/index.html')

        else:
            return render(request, 'homepage/index.html')


def contactus_view(request):

    if request.method == 'GET':
        form = ContactusForm()
    else:
        form = ContactusForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data['Email']
            name = form.cleaned_data['Name']
            # phone=form.cleaned_data['Phone']
            message = form.cleaned_data['Message']
            send_mail(name, message, email, [
                      'armantiwari1123@gmail.com'], fail_silently=False)
            return render(request, 'contactus/contactussuccess.html')
    return render(request, 'contactus/contactus.html', {'form': form})


def admin_ui(request):

    if request.method == 'GET':

        if request.user.is_authenticated:

            auser = request.user
            Feedbackobj = Feedback.objects.all()

            return render(request, 'admin/admin_ui/admin_ui.html', {"auser": auser, "Feedback": Feedbackobj})

        else:
            return redirect('home')

    if request.method == 'POST':

        return render(request, 'patient/patient_ui/profile.html')



def patient_ui(request):

    if request.method == 'GET':

        if request.user.is_authenticated:

            patientusername = request.session['patientusername']
            Feedbackobj = Feedback.objects.all()
            puser = User.objects.get(username=patientusername)
            n = notification.objects.filter(patient=puser.patient)
            return render(request, 'patient/patient_ui/profile.html', {"puser": puser, "Feedback": Feedbackobj, "notification": n})

        else:
            return redirect('home')

    if request.method == 'POST':

        return render(request, 'patient/patient_ui/profile.html')


def pviewprofile(request, patientusername):

    if request.method == 'GET':
        # doctor ko detail patient ko maa dekhouna ko laagi
        # duser = User.objects.get(username=doctorusername)
        # feedback/notification dekhoun ko laagi
        Feedbackobj = Feedback.objects.all()

        puser = User.objects.get(username=patientusername)
        n = notification.objects.filter(patient=puser.patient)
        return render(request, 'patient/view_profile/view_profile.html', {"puser": puser, "Feedback": Feedbackobj, "notification": n})

# patient profile view by doctor


def pviewprofiled(request, patientusername):

    if request.method == 'GET':

        puser = User.objects.get(username=patientusername)

        return render(request, 'patient/view_profile/view_profiled.html', {"puser": puser})


# doctor profile view by patient

def dviewprofilep(request, doctorusername):

    if request.method == 'GET':

        duser = User.objects.get(username=doctorusername)
        r = rating_review.objects.filter(doctor=duser.doctor)
        p = consultingpayment.objects.filter(doctor=duser.doctor)

        return render(request, 'doctor/view_profile/view_profilep.html', {"duser": duser, "rate": r, "pay": p})


# check disease by  doctor

def checkdiseasebyDoc(request):

    diseaselist = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer disease', 'AIDS', 'Diabetes ',
                   'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine', 'Cervical spondylosis', 'Paralysis (brain hemorrhage)',
                   'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
                   'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
                   'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
                   'Arthritis', '(vertigo) Paroymsal  Positional Vertigo', 'Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']

    symptomslist = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
                    'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination',
                    'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy',
                    'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating',
                    'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes',
                    'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
                    'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
                    'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
                    'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
                    'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
                    'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
                    'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
                    'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
                    'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
                    'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
                    'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
                    'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
                    'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
                    'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum',
                    'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
                    'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
                    'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf',
                    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
                    'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
                    'yellow_crust_ooze']

    alphabaticsymptomslist = sorted(symptomslist)

    if request.method == 'GET':

        return render(request, 'patient/checkdiseasebyDoc/checkdiseasebyDoc.html', {"list2": alphabaticsymptomslist})

    elif request.method == 'POST':

        # access you data by playing around with the request.POST object

        inputno = int(request.POST["noofsym"])
        print(inputno)
        if (inputno == 0):
            return JsonResponse({'predicteddisease': "none", 'confidencescore': 0})

        else:

            psymptoms = []
            psymptoms = request.POST.getlist("symptoms[]")

            print(psymptoms)

            """      #main code start from here...
        """

            testingsymptoms = []
            # append zero in all coloumn fields...
            for x in range(0, len(symptomslist)):
                testingsymptoms.append(0)

            # update 1 where symptoms gets matched...
            for k in range(0, len(symptomslist)):

                for z in psymptoms:
                    if (z == symptomslist[k]):
                        testingsymptoms[k] = 1

            inputtest = [testingsymptoms]

            print(inputtest)

            predicted = model.predict(inputtest)
            print("predicted disease is : ")
            print(predicted)

            y_pred_2 = model.predict_proba(inputtest)
            confidencescore = y_pred_2.max() * 100
            print(" confidence score of : = {0} ".format(confidencescore))

            confidencescore = format(confidencescore, '.0f')
            predicted_disease = predicted[0]

            doctorusername = request.session['doctorusername']
            puser = User.objects.get(username=doctorusername)

            # saving to database.....................

            diseasename = predicted_disease
            no_of_symp = inputno
            symptomsname = psymptoms
            confidence = confidencescore

            diseaseinfo_new = diseaseinfo(
                diseasename=diseasename, no_of_symp=no_of_symp, symptomsname=symptomsname, confidence=confidence)
            diseaseinfo_new.save()

            request.session['diseaseinfo_id'] = diseaseinfo_new.id

            print("disease record saved sucessfully.............................")

            return JsonResponse({'predicteddisease': predicted_disease, 'confidencescore': confidencescore})

@login_required(login_url='sign_in_patient')
def checkdisease(request):

    diseaselist = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer disease', 'AIDS', 'Diabetes ',
                   'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine', 'Cervical spondylosis', 'Paralysis (brain hemorrhage)',
                   'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
                   'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
                   'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
                   'Arthritis', '(vertigo) Paroymsal  Positional Vertigo', 'Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']

    symptomslist = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
                    'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination',
                    'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy',
                    'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating',
                    'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes',
                    'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
                    'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
                    'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
                    'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
                    'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
                    'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
                    'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
                    'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
                    'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
                    'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
                    'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
                    'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
                    'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
                    'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum',
                    'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
                    'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
                    'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf',
                    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
                    'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
                    'yellow_crust_ooze']

    alphabaticsymptomslist = sorted(symptomslist)

    if request.method == 'GET':

        return render(request, 'patient/checkdisease/checkdisease.html', {"list2": alphabaticsymptomslist})

    elif request.method == 'POST':

        # access you data by playing around with the request.POST object

        inputno = int(request.POST["noofsym"])
        print(inputno)
        if (inputno == 0):
            return JsonResponse({'predicteddisease': "none", 'confidencescore': 0})

        else:

            psymptoms = []
            psymptoms = request.POST.getlist("symptoms[]")

            print(psymptoms)

            """      #main code start from here...
        """

            testingsymptoms = []
            # append zero in all coloumn fields...
            for x in range(0, len(symptomslist)):
                testingsymptoms.append(0)

            # update 1 where symptoms gets matched...
            for k in range(0, len(symptomslist)):

                for z in psymptoms:
                    if (z == symptomslist[k]):
                        testingsymptoms[k] = 1

            inputtest = [testingsymptoms]

            print(inputtest)

            predicted = model.predict(inputtest)
            print("predicted disease is : ")
            print(predicted)

            y_pred_2 = model.predict_proba(inputtest)
            confidencescore = y_pred_2.max() * 100
            print(" confidence score of : = {0} ".format(confidencescore))

            confidencescore = format(confidencescore, '.0f')
            predicted_disease = predicted[0]

            # consult_doctor codes----------

            #   doctor_specialization = ["Rheumatologist","Cardiologist","ENT specialist","Orthopedist","Neurologist",
            #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist"]

            Rheumatologist = ['Osteoarthristis', 'Arthritis']

            Cardiologist = ['Heart attack',
                            'Bronchial Asthma', 'Hypertension' ]

            ENT_specialist = [
                '(vertigo) Paroymsal  Positional Vertigo', 'Hypothyroidism']

            Orthopedist = []

            Neurologist = [
                'Varicose veins', 'Paralysis (brain hemorrhage)', 'Migraine', 'Cervical spondylosis']

            Allergist_Immunologist = ['Allergy', 'Pneumonia',
                                      'AIDS', 'Common Cold', 'Tuberculosis', 'Malaria', 'Dengue', 'Typhoid']

            Urologist = ['Urinary tract infection',
                         'Dimorphic hemmorhoids(piles)']

            Dermatologist = ['Acne', 'Chicken pox',
                             'Fungal infection', 'Psoriasis', 'Impetigo']

            Gastroenterologist = ['Peptic ulcer disease', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Gastroenteritis', 'Hepatitis E',
                                  'Alcoholic hepatitis', 'Jaundice', 'hepatitis A',
                                  'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Diabetes ', 'Hypoglycemia']

            #  hospitallist=['National Center for Rheumatic Diseases ','Vayodha Hospitals','Nepal Mediciti','Grande International Hospital','NEPAL ORTHOPAEDIC HOSPITAL','Shahid Gangalal National Heart Center','Gautam Buddha Int\'l Cardiac Hospital','National Cardiac Centre','Vayodha Hospitals','Norvic International Hospital']

            if predicted_disease in Rheumatologist:

                consultdoctor = "Rheumatologist"
                consulthospital = ['National Center for Rheumatic Diseases ', 'Vayodha Hospitals',
                                   'Nepal Mediciti', 'Grande International Hospital', 'NEPAL ORTHOPAEDIC HOSPITAL']
                consulthospital1 = "National Center for Rheumatic Diseases "
                consulthospital2 = "Vayodha Hospitals"
                consulthospital3 = "Nepal Mediciti"
                consulthospital4 = "Grande International Hospital"
                consulthospital5 = "NEPAL ORTHOPAEDIC HOSPITAL"

            if predicted_disease in Cardiologist:
                consultdoctor = "Cardiologist"
                consulthospital = ['Shahid Gangalal National Heart Center', 'Gautam Buddha Int\'l Cardiac Hospital',
                                   'National Cardiac Centre', 'Vayodha Hospitals', 'Norvic International Hospital']
                consulthospital1 = "Shahid Gangalal National Heart Center"
                consulthospital2 = "Gautam Buddha Int\'l Cardiac Hospital"
                consulthospital3 = "National Cardiac Centre"
                consulthospital4 = "Vayodha Hospitals"
                consulthospital5 = "Norvic International Hospital"

            elif predicted_disease in ENT_specialist:
                consultdoctor = "ENT specialist"
                consulthospital = ['Kathmandu ENT Hospital Pvt. Ltd.',
                                   'MANIPAL TEACHING HOSPITAL (MTH)', 'ENT & Endocrine Clinic SHANKHAMUL', 'National ENT Centre', 'Grande International Hospital']
                consulthospital1 = "Kathmandu ENT Hospital Pvt. Ltd."
                consulthospital2 = "MANIPAL TEACHING HOSPITAL (MTH)"
                consulthospital3 = "ENT & Endocrine Clinic SHANKHAMUL"
                consulthospital4 = "National ENT Centre"
                consulthospital5 = "Grande International Hospital"

            elif predicted_disease in Orthopedist:
                consultdoctor = "Orthopedist"
                consulthospital = ['NEPAL ORTHOPAEDIC HOSPITAL', 'Grande International Hospital',
                                   'Manual Therapy Hospital Pvt Ltd (MT Hospital)', 'Star Hospital Limited']
                consulthospital1 = "NEPAL ORTHOPAEDIC HOSPITAL"
                consulthospital2 = "Grande International Hospital"
                consulthospital3 = "Manual Therapy Hospital Pvt Ltd (MT Hospital)"
                consulthospital4 = "Star Hospital Limited"
                consulthospital5 = "Medanta Ortho & Neuro Care Center"

            elif predicted_disease in Neurologist:
                consultdoctor = "Neurologist"
                consulthospital = ['Annapurna Neuro Hospital', 'Upendra Devkota Memorial National Institute Of Neurological And Allied Sciences',
                                   'Tinau International Hospital Pvt.Ltd.', ' Neuro & Trauma Research Center', 'Mother & Child Hospital ( Neuro Hospital )', 'Neuro and Allied Clinic']
                consulthospital1 = "Annapurna Neuro Hospital"
                consulthospital2 = "Upendra Devkota Memorial National Institute Of Neurological And Allied Sciences"
                consulthospital3 = "Tinau International Hospital Pvt.Ltd."
                consulthospital4 = "Neuro & Trauma Research Center"
                consulthospital5 = "Neuro and Allied Clinic"

            elif predicted_disease in Allergist_Immunologist:
                consultdoctor = "Allergist/Immunologist"
                consulthospital = ['Clinic One Kathmandu', 'Niroginepal', 'Om Hospital & Research Center',
                                   'Om Hospital & Research Center', 'शुक्रराज ट्रपिकल तथा सरुवा रोग अस्पताल', 'Charak Memorial Hospital']
                consulthospital1 = "Clinic One Kathmandu"
                consulthospital2 = "Niroginepal"
                consulthospital3 = "Om Hospital & Research Center"
                consulthospital4 = "शुक्रराज ट्रपिकल तथा सरुवा रोग अस्पताल"
                consulthospital5 = "Charak Memorial Hospital"

            elif predicted_disease in Urologist:
                consultdoctor = "Urologist"
                consulthospital = ['Vayodha Hospitals', 'Bir Hospital', 'Grande International Hospital',
                                   'Civil Service Hospital Of Nepal', 'Norvic International Hospital']
                consulthospital1 = "Vayodha Hospitals"
                consulthospital2 = "Grande International Hospital"
                consulthospital3 = "Civil Service Hospital Of Nepal"
                consulthospital4 = "Bir Hospital"
                consulthospital5 = "Norvic International Hospital"

            elif predicted_disease in Dermatologist:
                consultdoctor = "Dermatologist"
                consulthospital = ['The Skin Clinic by Dr.Jebina Lama', 'Nepal Korea SkinCare Hospital',
                                   'Nepal Skin Care Center', 'DI Skin Health and Referral Center(DISHARC)', 'Nepal Skin Hospital Pvt Ltd']
                consulthospital1 = "The Skin Clinic by Dr.Jebina Lama"
                consulthospital2 = "Nepal Korea SkinCare Hospital"
                consulthospital3 = "Nepal Skin Care Center"
                consulthospital4 = "DI Skin Health and Referral Center(DISHARC)"
                consulthospital5 = "Nepal Skin Hospital Pvt Ltd"

            elif predicted_disease in Gastroenterologist:
                consultdoctor = "Gastroenterologist"
                consulthospital = [
                    '\nGrande International Hospital \n' 'Nepal Mediciti \n' 'HAMS Hospital \n ' 'Bir Hospital \n' 'Kantipur Hospital \n']
                consulthospital1 = "Grande International Hospital"
                consulthospital2 = "Nepal Mediciti"
                consulthospital3 = "HAMS Hospital"
                consulthospital4 = "Bir Hospital"
                consulthospital5 = "Kantipur Hospital"

            else:
                consultdoctor = "other"
                consulthospital = ['Any Nearest Hospital']
                consulthospital1 = "Any Nearest Hospital"
                consulthospital2 = "Any Nearest Hospital"
                consulthospital3 = "Any Nearest Hospital"
                consulthospital4 = "Any Nearest Hospital"
                consulthospital5 = "Any Nearest Hospital"

            request.session['doctortype'] = consultdoctor

            patientusername = request.session['patientusername']
            puser = User.objects.get(username=patientusername)

            # saving to database.....................

            patient = puser.patient
            diseasename = predicted_disease
            no_of_symp = inputno
            symptomsname = psymptoms
            confidence = confidencescore

            diseaseinfo_new = diseaseinfo(patient=patient, diseasename=diseasename, no_of_symp=no_of_symp, symptomsname=symptomsname, confidence=confidence, consultdoctor=consultdoctor, consulthospital=consulthospital,
                                          consulthospital1=consulthospital1, consulthospital2=consulthospital2, consulthospital3=consulthospital3, consulthospital4=consulthospital4, consulthospital5=consulthospital5)
            diseaseinfo_new.save()

            request.session['diseaseinfo_id'] = diseaseinfo_new.id

            print("disease record saved sucessfully.............................")

            return JsonResponse({'predicteddisease': predicted_disease, 'confidencescore': confidencescore, "consultdoctor": consultdoctor, "consulthospital": consulthospital, "consulthospital1": consulthospital1, "consulthospital2": consulthospital2, "consulthospital3": consulthospital3, "consulthospital4": consulthospital4, "consulthospital5": consulthospital5})


def pconsultation_history(request):

    if request.method == 'GET':

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        patient_obj = puser.patient
        p = consultingpayment.objects.filter(patient=puser.patient)
        consultationnew = consultation.objects.filter(patient=patient_obj)

        return render(request, 'patient/consultation_history/consultation_history.html', {"consultation": consultationnew,"payment":p})


def dconsultation_history(request):

    if request.method == 'GET':

        doctorusername = request.session['doctorusername']
        duser = User.objects.get(username=doctorusername)
        doctor_obj = duser.doctor

        p = consultingpayment.objects.filter(doctor=duser.doctor)
        consultationnew = consultation.objects.filter(doctor=doctor_obj)
        # reportuploadnew=reportupload.objects.filter(doctor=doctor_obj)
        paginator = Paginator(consultationnew, 3)
        page_number = request.GET.get('page1')

        try:
            consultation_list = paginator.page(page_number)
        except PageNotAnInteger:
            consultation_list = paginator.page(1)
        except EmptyPage:
            consultation_list = paginator.page(paginator.num_pages)
        # consultation_list=paginator.get_page(page_number)

        # paginator = Paginator(p, 3)
        # page_number = request.GET.get('page2')

        # # pay_list=paginator1.get_page(page_number1)
        # try:
        #     pay_list = paginator.page(page_number)
        # except PageNotAnInteger:
        #     pay_list = paginator.page(1)
        # except EmptyPage:
        #     pay_list = paginator.page(paginator.num_pages)

        return render(request, 'doctor/consultation_history/consultation_history.html', {"consultation": consultation_list})


def doctor_ui(request):

    if request.method == 'GET':

        doctorid = request.session['doctorusername']
        duser = User.objects.get(username=doctorid)

        return render(request, 'doctor/doctor_ui/profile.html', {"duser": duser})


def dviewprofile(request, doctorusername):

    if request.method == 'GET':

        duser = User.objects.get(username=doctorusername)
        r = rating_review.objects.filter(doctor=duser.doctor)
        # doctor ko profile maa consultpayment dekhouna lai..utaa  doctor ko viewprofile maa for loop lagayerw value tanna lai
        p = consultingpayment.objects.filter(doctor=duser.doctor)

        return render(request, 'doctor/view_profile/view_profile.html', {"duser": duser, "rate": r, "pay": p})


def consult_a_doctor(request):

    if request.method == 'GET':

        doctortype = request.session['doctortype']
        print(doctortype)
        # dobj = doctor.objects.all()
        dobj = doctor.objects.filter(specialization=doctortype)
        

        return render(request, 'patient/consult_a_doctor/consult_a_doctor.html', {"dobj": dobj})



def book_consultation(request):

    if request.method == 'GET':
       
        duser = doctor.objects.all()
      

        return render(request, 'patient/book_consultation/book_consultation.html', {"dobj": duser})

@login_required(login_url='sign_in_patient')
def make_consultation(request, doctorusername):

    if request.method == 'POST':

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        patient_obj = puser.patient

        # doctorusername = request.session['doctorusername']
        duser = User.objects.get(username=doctorusername)
        doctor_obj = duser.doctor
        request.session['doctorusername'] = doctorusername

        diseaseinfo_id = request.session['diseaseinfo_id']
        diseaseinfo_obj = diseaseinfo.objects.get(id=diseaseinfo_id)

        consultation_date = date.today()
        amount = 200

        status = "closed"

        consultation_new = consultation(patient=patient_obj, doctor=doctor_obj,
                                        diseaseinfo=diseaseinfo_obj, consultation_date=consultation_date, amount=amount, status=status)
        consultation_new.save()

        request.session['consultation_id'] = consultation_new.id

        print("consultation record is saved sucessfully.............................")

        return redirect('consultationview', consultation_new.id)


def consultationview(request, consultation_id):

    if request.method == 'GET':
        consultation_obj = consultation.objects.get(id=consultation_id)

        r = rating_review.objects.filter(doctor=consultation_obj.doctor)
        request.session['consultation_id'] = consultation_id
        consultation_obj = consultation.objects.get(id=consultation_id)
        report_o=reportupload.objects.filter(doctor=consultation_obj.doctor,patient=consultation_obj.patient,diseaseinfo=consultation_obj.diseaseinfo)
      
        # doctorusername = request.session['doctorusername']
        # duser = User.objects.get(username=doctorusername)

        # r = rating_review.objects.filter(doctor=duser.doctor)

        return render(request, 'consultation/consultation.html', {"consultation": consultation_obj, "rate": r,"report_obj":report_o})


def rate_review(request, consultation_id):
    if request.method == "POST":

        consultation_obj = consultation.objects.get(id=consultation_id)
        patient_id = consultation_obj.patient
        doctor_id = consultation_obj.doctor
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        if rating_review.objects.filter(patient_id=patient_id,doctor_id=doctor_id).exists():
              
                messages.error(request, 'You have already rated the doctor!!!')
                return redirect('consultationview', consultation_id)
                
        else:
            rating_obj = rating_review(
            patient=patient_id, doctor=doctor_id, rating=rating, review=review)
            rating_obj.save()
            messages.info(request, 'Rated Successfully!!!')

            rate = rating_obj.rating_is
            doctor.objects.filter(pk=doctor_id).update(rating=rate)

            return redirect('consultationview', consultation_id)



def consultpayment(request, consultation_id):
    if request.method == "POST":

        consultation_obj = consultation.objects.get(id=consultation_id)
        patient = consultation_obj.patient
        doctor1 = consultation_obj.doctor
        
        paying = request.POST.get('paying')
        bank = request.POST.get('bank')
        accountno = request.POST.get('accountno')
       

        status = "Pending"
        diseaseinfo_id = request.session['diseaseinfo_id']
        diseaseinfo_obj = diseaseinfo.objects.get(id=diseaseinfo_id)
        pm = request.POST.get("payment_method")

        if pm == "Khalti":
            if consultingpayment.objects.filter(consultation=consultation_obj.id).exists():
                messages.error(request, 'You have already paid the consultation fee!!!')
                return redirect('consultationview', consultation_id)

            else:
                messages.success(request, 'Your Fund has been successfully transferred.')
                paying_obj = consultingpayment(consultation=consultation_obj,patient=patient, doctor=doctor1, paying=paying,
                                           status=status,diseaseinfo=diseaseinfo_obj, payment_method=pm)
                paying_obj.save()
                return redirect('khaltirequest', consultation_obj.id)
            # return redirect(reverse("khaltirequest") + "?c_id=" + str(consultation_obj.id))
        elif pm == "Esewa":
            if consultingpayment.objects.filter(consultation=consultation_obj.id).exists():
                messages.error(request, 'You have already paid the consultation fee!!!')
                return redirect('consultationview', consultation_id)
            else:
                messages.success(request, 'Your Fund has been successfully transferred.')    
                paying_obj = consultingpayment(consultation=consultation_obj,patient=patient, doctor=doctor1, paying=paying,
                                           status=status,diseaseinfo=diseaseinfo_obj, payment_method=pm)
                paying_obj.save()
                return redirect('esewarequest', consultation_obj.id)
            # return redirect(reverse("main_app:esewarequest") + "?c_id=" + str(consultation_obj.id))
        # else:
        #     return redirect("home")

        else:
            if consultingpayment.objects.filter(consultation=consultation_obj.id).exists():
              
                messages.error(request, 'You have already paid the consultation fee!!!')
                return redirect('consultationview', consultation_id)
            else:
                messages.success(request, 'Your Fund has been successfully transferred.')   
                paying_obj = consultingpayment(consultation=consultation_obj,patient=patient, doctor=doctor1, paying=paying, bank=bank, accountno=accountno,
                                       status=status,diseaseinfo=diseaseinfo_obj, payment_method=pm)
                paying_obj.save()

        pay = int(paying_obj.paying_is)
        doctor.objects.filter(pk=doctor1).update(paying=pay)
        return redirect('consultationview', consultation_id)



def paymentview(request, consultation_id):

    if request.method == 'GET':
        consultation_obj = consultation.objects.get(id=consultation_id)

        r = rating_review.objects.filter(doctor=consultation_obj.doctor)
        request.session['consultation_id'] = consultation_id
        consultation_obj = consultation.objects.get(id=consultation_id)
        report_o=reportupload.objects.filter(doctor=consultation_obj.doctor,patient=consultation_obj.patient,diseaseinfo=consultation_obj.diseaseinfo)
        payment_o=consultingpayment.objects.filter(doctor=consultation_obj.doctor,patient=consultation_obj.patient,diseaseinfo=consultation_obj.diseaseinfo)
        # payment_o = consultingpayment.objects.get(id=consultation_id)
        # doctorusername = request.session['doctorusername']
        # duser = User.objects.get(username=doctorusername)

        # r = rating_review.objects.filter(doctor=duser.doctor)

        return render(request, 'payment/payment_detail.html', {"consultation": consultation_obj, "rate": r,"report_obj":report_o,"payment_obj":payment_o})

def notify_a_patient(request, consultation_id):
    if request.method == "POST":

        consultation_obj = consultation.objects.get(id=consultation_id)
        patient = consultation_obj.patient
        doctor1 = consultation_obj.doctor

        description = request.POST.get('description')
        consultationDateTime = request.POST.get('consultationDateTime')

        notify_obj = notification(consultation=consultation_obj,patient=patient, doctor=doctor1,
                                  description=description, consultationDateTime=consultationDateTime)
        messages.success(request,'Consultation date scheduled successfully')
        notify_obj.save()
        # pay = int(paying_obj.paying_is)
        # doctor.objects.filter(pk=doctor1).update(paying=pay)
        # return redirect('home')
        # return HttpResponseRedirect("")  
        # return redirect('')
        return redirect('dconsultation_history')





# def dateDiffInSeconds(date1, date2):
#   timedelta = date2 - date1
#   return timedelta.days * 24 * 3600 + timedelta.seconds

# def daysHoursMinutesSecondsFromSeconds(seconds):
# 	minutes, seconds = divmod(seconds, 60)
# 	hours, minutes = divmod(minutes, 60)
# 	days, hours = divmod(hours, 24)
# 	return (days, hours, minutes, seconds)

# req = notification.consultationDateTime

# now = datetime.now()

# while req>now:
#     print("%dd %dh %dm %ds" % daysHoursMinutesSecondsFromSeconds(dateDiffInSeconds(now, req)))
#     sleep(1)
#     now = datetime.now()

# print("Done")








def uploading_report(request, consultation_id):
    if request.method == "POST":

        consultation_obj = consultation.objects.get(id=consultation_id)
        patient = consultation_obj.patient
        doctor1 = consultation_obj.doctor
      
        description = request.POST.get('description')
        report_pics = request.FILES.getlist('report_pics')
        diseaseinfo_id = request.session['diseaseinfo_id']
        diseaseinfo_obj = diseaseinfo.objects.get(id=diseaseinfo_id)
        for report_pic in report_pics:
            reportupload.objects.create(patient=patient, doctor=doctor1,
                                      description=description, report_pics=report_pic,diseaseinfo=diseaseinfo_obj)


        # reportupload.objects.create(patient=patient, doctor=doctor1,
        #                               description=description, report_pics=report_pics)
        messages.info(request,'Report Uploaded sucessfully')    

        return redirect('consultationview', consultation_id)


def KhaltiRequestView(request, consultation_id):

    if request.method == 'GET':

        request.session['consultation_id'] = consultation_id
        consultation_obj = consultation.objects.get(id=consultation_id)

        return render(request, "khaltirequest.html", {"consultation": consultation_obj})


# class KhaltiRequestView(View):
#     def get(self, request,**kwargs):
#         c_id = request.GET.get("consultation_id")

#         consultation_obj = consultation.objects.get(id=c_id)
#         context = {
#             "consultation_obj": consultation_obj
#         }
#         return render(request, "khaltirequest.html", context)


class KhaltiVerifyView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        amount = request.GET.get("amount")
        c_id = request.GET.get("consultation_id")
        print(token, amount, c_id)

        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": "Key test_secret_key_02b924fa8e924217ac852cedd2670f93"
        }

        consultation_obj = consultation.objects.get(id=c_id)

        response = requests.post(url, payload, headers=headers)
        resp_dict = response.json()
        if resp_dict.get("idx"):
            success = True
            consultation_obj.payment_completed = True
            consultation_obj.save()
        else:
            success = False
        data = {
            "success": success
        }
        return JsonResponse(data)


def EsewaRequestView(request, consultation_id):
    if request.method == 'GET':
        request.session['consultation_id'] = consultation_id
        consultation_obj = consultation.objects.get(id=consultation_id)
        return render(request, "esewarequest.html", {"consultation": consultation_obj})

# class EsewaRequestView(View):
#     def get(self, request, *args, **kwargs):
#         c_id = request.GET.get("consultation_id")
#         consultation_obj = consultation.objects.get(id=c_id)
#         context = {
#             "consultation_obj": consultation_obj
#         }
#         return render(request, "esewarequest.html", context)


class EsewaVerifyView(View):
    def get(self, request, *args, **kwargs):
        # def EsewaVerifyView(request, consultation_id):
        #     if request.method == 'GET':
        import xml.etree.ElementTree as ET
        oid = request.GET.get("oid")
        amt = request.GET.get("amt")
        refId = request.GET.get("refId")
        print(oid, amt, refId)
        url = "https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': amt,
            'scd': 'EPAYTEST',
            'rid': refId,
            'pid': oid,
        }
        resp = requests.post(url, d)
        root = ET.fromstring(resp.content)
        print(root[0].text)
        status = root[0].text.strip()
        print(status)

        consultation_id = oid
        consultation_obj = consultation.objects.get(id=consultation_id)
        if status == "Success":
            consultation_obj.payment_completed = True
            consultation_obj.save()

            return redirect("/")

        else:

            return redirect("/esewa-request/"+consultation_id)


def verify_payment(request, consultation_id):
    if request.method == "POST":

        consultingpayment.objects.filter(
            pk=consultation_id).update(status="Verified")
        #  return render('doctor/view_profile/view_profile.html' )
        # return HttpResponseRedirect("")  
        return redirect('home')




def close_consultation(request, consultation_id):
    if request.method == "POST":

        consultation.objects.filter(pk=consultation_id).update(status="closed")

        return redirect('home')


def start_consultation(request, consultation_id):
    if request.method == "POST":

        consultation.objects.filter(pk=consultation_id).update(status="active")

        return redirect('consultationview', consultation_id)
       

# -----------------------------chatting system ---------------------------------------------------


def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)

        consultation_id = request.session['consultation_id']
        consultation_obj = consultation.objects.get(id=consultation_id)
        # patient = consultation_obj.patient
        # doctor1 = consultation_obj.doctor

        c = Chat(consultation_id=consultation_obj,
                 sender=request.user, message=msg)

        #msg = c.user.username+": "+msg

        if msg != '':
            c.save()
            print("msg saved" + msg)
            return JsonResponse({'msg': msg})
    else:
        return HttpResponse('Request must be POST.')


def chat_messages(request):
    if request.method == "GET":

        consultation_id = request.session['consultation_id']
       
        c = Chat.objects.filter(consultation_id=consultation_id)
        return render(request, 'consultation/chat_body.html', {'chat': c})


# -----------------------------chatting system ---------------------------------------------------
class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = doctor.objects.filter(
            Q(name__icontains=kw) | Q(practicinghospital__icontains=kw) | Q(mobile_no__icontains=kw)| Q(specialization__icontains=kw))
        print(results)
        context["results"] = results
        return context

def ppayment_history(request):

    if request.method == 'GET':

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        patient_obj = puser.patient
       # p = consultingpayment.objects.filter(patient=puser.patient)
        paymentnew = consultingpayment.objects.filter(patient=patient_obj)
        paginator = Paginator(paymentnew, 5)
        page_number = request.GET.get('page1')

        try:
            payment_list = paginator.page(page_number)
        except PageNotAnInteger:
            payment_list = paginator.page(1)
        except EmptyPage:
            payment_list = paginator.page(paginator.num_pages)

        return render(request, 'patient/payment_history/payment_history.html', {"payment": payment_list})

        
def dpayment_history(request):

    if request.method == 'GET':

        doctorusername = request.session['doctorusername']
        duser = User.objects.get(username=doctorusername)
        doctor_obj = duser.doctor

        # p = consultingpayment.objects.filter(doctor=duser.doctor)
        paymentnew = consultingpayment.objects.filter(doctor=doctor_obj)
       
        paginator = Paginator(paymentnew, 5)
        page_number = request.GET.get('page1')

        try:
            payment_list = paginator.page(page_number)
        except PageNotAnInteger:
            payment_list = paginator.page(1)
        except EmptyPage:
            payment_list = paginator.page(paginator.num_pages)

        return render(request, 'doctor/payment_history/payment_history.html', {"payment": payment_list})