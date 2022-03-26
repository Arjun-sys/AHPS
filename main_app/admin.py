from django.contrib import admin
from .models import consultingpayment, patient , doctor , diseaseinfo , consultation,rating_review, reportupload

# Register your models here.
# admin.site.register(approval)
admin.site.register(patient)
admin.site.register(doctor)
admin.site.register(diseaseinfo)
# admin.site.register(diseaseinfobyDoc)
admin.site.register(consultation)
admin.site.register(rating_review)
admin.site.register(consultingpayment)
admin.site.register(reportupload)