from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.home, name="home"),
    
#     path('sign_in_admin', views.sign_in_admin , name='sign_in_admin'),

#     path('signup_patient', views.signup_patient, name="signup_patient"),
#     path('sign_in_patient', views.sign_in_patient , name='sign_in_patient'),
#     path('savepdata/<str:patientusername>', views.savepdata , name='savepdata'),
    

#     path('signup_doctor', views.signup_doctor , name="signup_doctor"),
#     path('sign_in_doctor', views.sign_in_doctor , name='sign_in_doctor'),

#     path('saveddata/<str:doctorusername>', views.saveddata , name='saveddata'),

 

#     path('savepaymentdata/<int:consultation_id>', views.savepaymentdata , name='savepaymentdata'),
#     path('logout', views.logout , name='logout'),


    path('admin_ui', views.admin_ui, name='admin_ui'),
    path('contactus', views.contactus_view, name='contactus'),

    path('patient_ui', views.patient_ui, name='patient_ui'),
    path('checkdisease', views.checkdisease, name="checkdisease"),


    # check disease by doctor
    path('checkdiseasebyDoc', views.checkdiseasebyDoc, name="checkdiseasebyDoc"),

    path('pviewprofile/<str:patientusername>',
         views.pviewprofile, name='pviewprofile'),



    # View profile of patient by doctor
    path('pviewprofiled/<str:patientusername>',
         views.pviewprofiled, name='pviewprofiled'),
    # View profile of doctor by patient
    path('dviewprofilep/<str:doctorusername>',
         views.dviewprofilep, name='dviewprofilep'),


    path('pconsultation_history', views.pconsultation_history,
         name='pconsultation_history'),
    path('consult_a_doctor', views.consult_a_doctor, name='consult_a_doctor'),
    path('book_consultation', views.book_consultation, name='book_consultation'),
  
    path('make_consultation/<str:doctorusername>',
         views.make_consultation, name='make_consultation'),

    path('rate_review/<int:consultation_id>',
         views.rate_review, name='rate_review'),
    path('notify_a_patient/<int:consultation_id>',
         views.notify_a_patient, name='notify_a_patient'),
    path('uploading_report/<int:consultation_id>',
         views.uploading_report, name='uploading_report'),




    path('consultpayment/<int:consultation_id>',
         views.consultpayment, name='consultpayment'),
    path('verify_payment/<int:consultation_id>',
         views.verify_payment, name='verify_payment'),

    path('dconsultation_history', views.dconsultation_history,
         name='dconsultation_history'),
    path('dviewprofile/<str:doctorusername>',
         views.dviewprofile, name='dviewprofile'),
    path('doctor_ui', views.doctor_ui, name='doctor_ui'),



    path('consultationview/<int:consultation_id>',
         views.consultationview, name='consultationview'),
    path('paymentview/<int:consultation_id>',
         views.paymentview, name='paymentview'),


    path('close_consultation/<int:consultation_id>',
         views.close_consultation, name='close_consultation'),
    path('start_consultation/<int:consultation_id>',
         views.start_consultation, name='start_consultation'),


    path('post', views.post, name='post'),
    path('chat_messages', views.chat_messages, name='chat_messages'),
    path('khalti-request/<int:consultation_id>', views.KhaltiRequestView, name='khaltirequest'),
    path('khalti-verify/<int:consultation_id>', views.KhaltiVerifyView, name='khaltiverify'),
    path('khalti-verify/', views.KhaltiVerifyView.as_view(), name='khaltiverify'),

    path('esewa-request/<int:consultation_id>', views.EsewaRequestView, name='esewarequest'),
    path('esewa-verify/<int:consultation_id>', views.EsewaVerifyView, name='esewaverify'),
    path('esewa-verify/', views.EsewaVerifyView.as_view(), name='esewaverify'),

    path("search/", views.SearchView.as_view(), name="search"),
    path('dpayment_history', views.dpayment_history,
         name='dpayment_history'),
    path('ppayment_history', views.ppayment_history,
         name='ppayment_history'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

