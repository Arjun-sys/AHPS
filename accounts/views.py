from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib import messages
from django.contrib.auth.models import User , auth
from django.contrib.auth import authenticate, login, logout
from main_app.models import patient,doctor,consultingpayment,consultation
from datetime import datetime
from .utils import password_reset_token
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from .models import *
from .forms import *
from django.core.files.storage import FileSystemStorage
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from main_app.doctor_decorators import unauthenticated_doctor,allowed_users
from django.contrib.auth.decorators import login_required
# Create your views here.


   
def logout(request):
    auth.logout(request)
    request.session.pop('patientid', None)
    request.session.pop('doctorid', None)
    request.session.pop('adminid', None)
    return render(request,'homepage/index.html')




def login(request):
  

    if request.method == 'POST':

          username =  request.POST.get('username')
          password =  request.POST.get('password')
 
          user = auth.authenticate(username=username,password=password)

          if user is not None : 
              try:
                 if ( user.is_superuser == True ) :
                     auth.login(request,user)

                     return redirect('admin_ui')



                 if ( user.patient.is_patient == True and user.patient.is_doctor==False ) :
                     request.session['patientusername'] = user.username

                     auth.login(request,user)

                    
                     return redirect('patient_ui')
                
                 if( user.doctor.is_patient == False and user.doctor.is_doctor==True ) :
                     auth.login(request,user)
                  
                     request.session['doctorusername'] = user.username

                     return redirect('doctor_ui')

               

              except :
                  messages.info(request,'Please enter the correct username or password ')
                  return redirect('login')

          else :
             messages.info(request,'Please enter the correct username or password')
             return redirect('login')


    else :
      return render(request,'login.html')










def sign_in_admin(request):
  

    if request.method == 'POST':

          username =  request.POST.get('username')
          password =  request.POST.get('password')
 
          user = auth.authenticate(username=username,password=password)

          if user is not None :


          
             
              try:
                 if ( user.is_superuser == True ) :
                     auth.login(request,user)

                     return redirect('admin_ui')



                 if ( user.patient.is_patient == True and user.patient.is_doctor==False ) :
                     request.session['patientusername'] = user.username

                     auth.login(request,user)

                    
                     return redirect('patient_ui')
                
                 if( user.doctor.is_patient == False and user.doctor.is_doctor==True ) :
                     auth.login(request,user)
                  
                     request.session['doctorusername'] = user.username

                     return redirect('doctor_ui')

               

              except :
                  messages.info(request,'Please enter the correct username and password for a admin account.')
                  return redirect('sign_in_admin')


              # try:

              #   if ( user.doctor.is_doctor == True ) :
              #     auth.login(request,user)
                  
              #     request.session['doctorusername'] = user.username

              #     return redirect('doctor_ui')
               
              # except :
              #     messages.info(request,'invalid credentials')
              #     return redirect('sign_in_admin')

              
              # try:
              #    if ( user.patient.is_patient == True ) :
              #        auth.login(request,user)

              #        request.session['patientusername'] = user.username

              #        return redirect('patient_ui')
               
              # except :
              #     messages.info(request,'Please enter the correct username and password for a admin account.')
              #     return redirect('sign_in_admin')

            

          else :
             messages.info(request,'Please enter the correct username and password for a admin account.')
             return redirect('sign_in_admin')


    else :
      return render(request,'admin/signin/signin.html')


@unauthenticated_doctor
def signup_patient(request):


    if request.method == 'POST':
      
      if request.POST['username'] and request.POST['email'] and  request.POST['name']  and request.POST['dob'] and request.POST['gender'] and request.POST['address']and request.POST['mobile'] and request.FILES['profile_pic'] and request.POST.get('password')and request.POST.get('password1'):

          username =  request.POST['username']
          email =  request.POST['email']

          name =  request.POST['name']
          dob =  request.POST['dob']
        

          
          gender =  request.POST['gender']
          address =  request.POST['address']
          mobile_no = request.POST['mobile']

          #For images must use as  profile_pic = request.FILES["profile_pic"]
          profile_pic = request.FILES["profile_pic"]
         
          password =  request.POST.get('password')
          password1 =  request.POST.get('password1')

          if password == password1:
              if User.objects.filter(username = username).exists():
                messages.info(request,'username already taken')
                return redirect('signup_patient')

              elif User.objects.filter(email = email).exists():
                messages.info(request,'email already taken')
                return redirect('signup_patient')
                
              else :
                user = User.objects.create_user(username=username,password=password,email=email)   
                user.save()
                
                patientnew = patient(user=user,name=name,dob=dob,gender=gender,address=address,mobile_no=mobile_no,profile_pic=profile_pic)
                patientnew.save()
                messages.info(request,'user created sucessfully')
                
              return redirect('sign_in_patient')

          else:
            messages.info(request,'password not matching, please try again')
            return redirect('signup_patient')

      else :
        messages.info(request,'Please make sure all required fields are filled out correctly')
        return redirect('signup_patient') 


    
    else :
      return render(request,'patient/signup_Form/signup.html')



def sign_in_patient(request):
  

    if request.method == 'POST':

          username =  request.POST.get('username')
          password =  request.POST.get('password')
 
          user = auth.authenticate(username=username,password=password)

          if user is not None :
             
              try:
                 if ( user.patient.is_patient == True ) :
                     auth.login(request,user)

                     request.session['patientusername'] = user.username

                     return redirect('patient_ui')
               
              except :
                  messages.info(request,'invalid credentials')
                  return redirect('sign_in_patient')


          else :
             messages.info(request,'invalid credentials')
             return redirect('sign_in_patient')


    else :
      return render(request,'patient/signin_page/index.html')


def savepdata(request,patientusername):

  if request.method == 'POST':

      name =  request.POST['name']
      dob =  request.POST['dob']
      gender =  request.POST['gender']
      address =  request.POST['address']
      mobile_no = request.POST['mobile_no']
      profile_pic=request.FILES.get('profile_pic')
      print(type(profile_pic))
      print(profile_pic)
      print(dob)
      dobdate = datetime.strptime(dob,'%Y-%m-%d')

      puser = User.objects.get(username=patientusername)

      patient.objects.filter(pk=puser.patient).update(name=name,dob=dobdate,gender=gender,address=address,mobile_no=mobile_no,profile_pic=profile_pic)

      return redirect('pviewprofile',patientusername)







#doctors account...........operations......
    

def signup_doctor(request):

    if request.method == 'GET':
    
       return render(request,'doctor/signup_Form/signup.html')


    if request.method == 'POST':
      
      if request.POST['username'] and request.POST['email'] and  request.POST['name'] and request.FILES.get('profile_pic') and request.POST['dob'] and request.POST['gender'] and request.POST['address']and request.POST['mobile'] and request.POST['password']and request.POST['password1']  and  request.POST['registration_no'] and  request.POST['year_of_registration'] and  request.POST['qualification'] and  request.POST['practicinghospital'] and  request.POST['specialization'] and  request.POST['start_time'] and  request.POST['end_time']  :

          username =  request.POST['username']
          email =  request.POST['email']

          name =  request.POST['name']
          profile_pic = request.FILES["profile_pic"]
          dob =  request.POST['dob']
          gender =  request.POST['gender']
          address =  request.POST['address']
          mobile_no = request.POST['mobile']
          registration_no =  request.POST['registration_no']
          year_of_registration =  request.POST['year_of_registration']
          qualification =  request.POST['qualification']
          practicinghospital=  request.POST['practicinghospital']
          specialization =  request.POST['specialization']
          start_time=request.POST['start_time']
          end_time=request.POST['end_time']
          bank=request.POST['bank']
          accountno=request.POST['accountno']
       
          password =  request.POST.get('password')
          password1 =  request.POST.get('password1')

          if password == password1:
              if User.objects.filter(username = username).exists():
                messages.info(request,'username already taken')
                return redirect('signup_doctor')

              elif User.objects.filter(email = email).exists():
                messages.info(request,'email already taken')
                return redirect('signup_doctor')
                
              else :
                user = User.objects.create_user(username=username,password=password,email=email)   
                user.save()
                
                doctornew = doctor( user=user, name=name, dob=dob,profile_pic=profile_pic, gender=gender, address=address, mobile_no=mobile_no, registration_no=registration_no, year_of_registration=year_of_registration, qualification=qualification, practicinghospital=practicinghospital, specialization=specialization,start_time=start_time,end_time=end_time,bank=bank,accountno=accountno )
                doctornew.save()
                messages.info(request,'user created sucessfully')
                print("doctorcreated")
                
              return redirect('sign_in_doctor')

          else:
            messages.info(request,'password not matching, please try again')
            return redirect('signup_doctor')

      else :
        messages.info(request,'Please make sure all required fields are filled out correctly')
        return redirect('signup_doctor') 






def sign_in_doctor(request):

    if request.method == 'GET':
    
       return render(request,'doctor/signin_page/index.html')

  
    if request.method == 'POST':

          username =  request.POST.get('username')
          password =  request.POST.get('password')
 

          user = auth.authenticate(username=username,password=password)

          if user is not None :
              
              try:

                if ( user.doctor.is_doctor == True ) :
                  auth.login(request,user)
                  
                  request.session['doctorusername'] = user.username

                  return redirect('doctor_ui')
               
              except :
                  messages.info(request,'invalid credentials')
                  return redirect('sign_in_doctor')

          else :
             messages.info(request,'invalid credentials')
             return redirect('sign_in_doctor')


    else :
      return render(request,'doctor/signin_page/index.html')





def saveddata(request,doctorusername):

  if request.method == 'POST':

    name =  request.POST['name']
    dob =  request.POST['dob']
    profile_pic=request.FILES.get('profile_pic')
    gender =  request.POST['gender']
    address =  request.POST['address']
    mobile_no = request.POST['mobile_no']
    registration_no =  request.POST['registration_no']
    year_of_registration =  request.POST['year_of_registration']
    qualification =  request.POST['qualification']
    practicinghospital =  request.POST['practicinghospital']
    specialization =  request.POST['specialization']
    start_time=request.POST['start_time']
    end_time=request.POST['end_time']
    bank=request.POST['bank']
    accountno=request.POST['accountno']
    
    dobdate = datetime.strptime(dob,'%Y-%m-%d')
    yor = datetime.strptime(year_of_registration,'%Y-%m-%d')

    duser = User.objects.get(username=doctorusername)

    doctor.objects.filter(pk=duser.doctor).update( name=name,dob=dob,profile_pic=profile_pic, gender=gender, address=address, mobile_no=mobile_no, registration_no=registration_no, year_of_registration=yor, qualification=qualification, practicinghospital=practicinghospital, specialization=specialization ,start_time=start_time,end_time=end_time,bank=bank,accountno=accountno)

    return redirect('dviewprofile',doctorusername)




def savepaymentdata(request,consultation_id):

  if request.method == 'POST':
    consultation_obj = consultation.objects.get(id=consultation_id)
    patient = consultation_obj.patient
    doctor = consultation_obj.doctor
    paying = request.POST('paying')
    bank = request.POST('bank')
    accountno = request.POST('accountno')
    description=request.POST('description')
    consultationDateTime=request.POST('consultationDateTime')
    status= request.POST('status')
    paying_obj = consultingpayment(patient=patient,doctor=doctor,paying=paying,bank=bank,accountno=accountno,description=description,consultationDateTime=consultationDateTime,status=status)
    # paying_obj.save()
    pay = int(paying_obj.paying_is)
    doctor.objects.filter(pk=doctor).update(paying=pay)
    return redirect('consultationview',consultation_id)


class PasswordForgotView(FormView):
    template_name = "forgotpassword.html"
    form_class = PasswordForgotForm
    success_url = "/forgot-password/?m=s"

    def form_valid(self, form):
        # get email from user
        # global email
        email = form.cleaned_data.get("email")
        # get current host ip/domain
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        # global patient
        user = User.objects.get(email=email)
        # user = patient.user
        # send mail to the user with email
        text_content = 'Please Click the link below to reset your password. '
        html_content = url + "/password-reset/" + email + \
            "/" + password_reset_token.make_token(user) + "/"
        send_mail(
            'Password Reset Link | Advanced Health Prediction System',
            text_content +"\n"+ html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("passwordforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)
      

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        
        return super().form_valid(form)
         