from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models import Avg
from datetime import date

# Create your models here.


#user = models.OneToOneField(settings.AUTH_USER_MODEL)

class patient(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    is_patient = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
   
    name = models.CharField(max_length = 50)
    profile_pic= models.ImageField(null=True,blank=True,upload_to="pics/")
    dob = models.DateField()
    
    address = models.CharField(max_length = 100)
    mobile_no = models.CharField(max_length = 15)
    gender = models.CharField(max_length = 10)
    status=models.BooleanField(default=False)
    
    @property
    def age(self):
        today = date.today()
        db = self.dob
        age = today.year - db.year
        if today.month < db.month or today.month == db.month and today.day < db.day:
            age -= 1
        return age 



class doctor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=True)

    name = models.CharField(max_length = 50)
    dob = models.DateField()
    address = models.CharField(max_length = 100)
    mobile_no = models.CharField(max_length = 15)
    gender = models.CharField(max_length = 10)
    profile_pic= models.ImageField(null=True,blank=True,upload_to="doc_pics")
    registration_no = models.CharField(max_length = 20)
    year_of_registration = models.DateField()
    qualification = models.CharField(max_length = 20)
    practicinghospital = models.CharField(max_length = 200)
    specialization = models.CharField(max_length = 30)
    #start_time = models.CharField(max_length=10)
    # end_time = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    rating=models.FloatField(default=0.0)
    # rating = models.IntegerField(default=0)
    status=models.BooleanField(default=False)
#Consultation payment ko laagi add gareko
    paying=models.IntegerField(default=0)
    bank=models.CharField(max_length = 100)
    accountno=models.CharField(max_length = 20)





class diseaseinfo(models.Model):

    patient = models.ForeignKey(patient , null=True, on_delete=models.SET_NULL)

    diseasename = models.CharField(max_length = 200)
    no_of_symp = models.IntegerField()
    symptomsname = ArrayField(models.CharField(max_length=200))
    confidence = models.DecimalField(max_digits=5, decimal_places=2)
    consultdoctor = models.CharField(max_length = 200)
#   Added Suggested hospital 
    consulthospital = ArrayField(models.CharField(max_length=400))
    precaution=ArrayField(models.CharField(max_length=1000))
    consulthospital1 = models.CharField(max_length = 200)
    consulthospital2 = models.CharField(max_length = 200)
    consulthospital3= models.CharField(max_length = 200)
    consulthospital4 = models.CharField(max_length = 200)
    consulthospital5= models.CharField(max_length = 200)


    
# class diseaseinfobyDoc(models.Model):

#     patient = models.ForeignKey(patient , null=True, on_delete=models.SET_NULL)
#     doctor = models.ForeignKey(doctor , null=True, on_delete=models.SET_NULL)
#     diseasename = models.CharField(max_length = 200)
#     no_of_symp = models.IntegerField()
#     symptomsname = ArrayField(models.CharField(max_length=200))
#     confidence = models.DecimalField(max_digits=5, decimal_places=2)
 
class consultation(models.Model):

    patient = models.ForeignKey(patient ,null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(doctor ,null=True, on_delete=models.SET_NULL)
    # consultingpayment=models.OneToOneField(consultingpayment ,null=True, on_delete=models.SET_NULL)
    diseaseinfo = models.OneToOneField(diseaseinfo, null=True, on_delete=models.SET_NULL)
    consultation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 20)
    amount=models.IntegerField(default=200)
    payment_completed=models.BooleanField(default=False,null=True,blank=True)  
METHOD = (
    ("By Website", " By Website"),
    ("Khalti", "Khalti"),
    ("Esewa", "Esewa"),
)


    
class reportupload(models.Model):

    patient = models.ForeignKey(patient ,null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(doctor ,null=True, on_delete=models.SET_NULL)
    time=models.DateTimeField(auto_now_add=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=True)
    report_pics= models.FileField(null=True,blank=True,upload_to="report_pics")
    diseaseinfo = models.OneToOneField(diseaseinfo, null=True, on_delete=models.SET_NULL)

class consultingpayment(models.Model):

    patient = models.ForeignKey(patient ,null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(doctor ,null=True, on_delete=models.SET_NULL)
    time=models.DateTimeField(auto_now_add=True)
    consultation = models.OneToOneField(consultation, null=True, on_delete=models.SET_NULL)
    diseaseinfo = models.OneToOneField(diseaseinfo, null=True, on_delete=models.SET_NULL)
    # reportupload = models.OneToOneField(reportupload, null=True, on_delete=models.SET_NULL)
    paying = models.IntegerField(default=0)
    bank = models.TextField( blank=True ) 
    accountno = models.IntegerField(default=0)
    # description=models.TextField(max_length=500)
    status = models.CharField(max_length = 20)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="By Website")


    @property
    def paying_is(self):
        new_paying = 0
        paying_obj = consultingpayment.objects.filter(doctor=self.doctor)
        for i in paying_obj:
            new_paying += i.paying  
           
        return new_paying





class approval(models.Model):

    patient = models.ForeignKey(patient ,null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(doctor ,null=True, on_delete=models.SET_NULL)
    diseaseinfo = models.OneToOneField(diseaseinfo, null=True, on_delete=models.SET_NULL)
    consultation_date = models.DateField()
    status = models.CharField(max_length = 20)



class rating_review(models.Model):

    patient = models.ForeignKey(patient ,null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(doctor ,null=True, on_delete=models.SET_NULL)
    
    rating = models.FloatField(default=0.0)
    review = models.TextField( blank=True ) 

    @property
    def rating_is(self):
        # new_rating = 0
        # rating_obj = rating_review.objects.filter(doctor=self.doctor)
        # count=len(rating_obj)
        # for i in rating_obj:
        #     new_rating += i.rating
        # return (new_rating/count)
        # # new_rating = new_rating/len(rating_obj)
        # # new_rating = int(new_rating)

        rating_obj = rating_review.objects.filter(doctor=self.doctor).aggregate(rating_avg=Avg('rating'))
        return (rating_obj['rating_avg'])
        
       

class notification(models.Model):

    patient = models.ForeignKey(patient ,null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(doctor ,null=True, on_delete=models.SET_NULL)
    consultation = models.ForeignKey(consultation, null=True, on_delete=models.SET_NULL)
    time=models.DateTimeField(auto_now_add=True)
    description=models.TextField(max_length=500)
    consultationDateTime=models.DateTimeField()



   
