from django.urls import path, include
from . import views
from django.conf.urls import url
from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
  


    path('sign_in_admin', views.sign_in_admin , name='sign_in_admin'),
    path('login', views.login , name='login'),

    path('signup_patient', views.signup_patient, name="signup_patient"),
    path('sign_in_patient', views.sign_in_patient , name='sign_in_patient'),
    path('savepdata/<str:patientusername>', views.savepdata , name='savepdata'),
    

    path('signup_doctor', views.signup_doctor , name="signup_doctor"),
    path('sign_in_doctor', views.sign_in_doctor , name='sign_in_doctor'),

    path('saveddata/<str:doctorusername>', views.saveddata , name='saveddata'),

 

    path('savepaymentdata/<int:consultation_id>', views.savepaymentdata , name='savepaymentdata'),
    path('logout', views.logout , name='logout'),

    path("forgot-password/", views.PasswordForgotView.as_view(), name="passworforgot"),
    path("password-reset/<email>/<token>/",
         views.PasswordResetView.as_view(), name="passwordreset"),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)