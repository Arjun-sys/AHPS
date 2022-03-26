from django import forms
from django.forms import Form
from .models import patient, doctor, diseaseinfo, consultation, rating_review, consultingpayment
from django.contrib.auth.models import User
from . import models




#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30,required="Name")
    # Phone=forms.CharField(max_length=10)
    Email = forms.EmailField(required="Email")
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
