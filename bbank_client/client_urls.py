from django.urls import path
from bbank_client import client_views
import include


urlpatterns = [
    path('client_login/', client_views.client_login),
    path('client_forgetpassword/',client_views.client_forgetpassword),
    path('client_setpassword/', client_views.client_set_password),
    path('client_reset/', client_views.client_sendotp),
    path('client_feedback/', client_views.client_feedback),
    path('about_us/', client_views.aboutus),
    path('home/', client_views.home),
    path('registeration/', client_views.client_register),
    path('bbank_directory/',client_views.bbank_directory),
    path('client_bloodbankdetails/<int:id>',client_views.bloodbank_details),
    path('client_feedback/', client_views.client_feedback),
    path('client_appointment/<int:id>',client_views.client_appointment),
    path('feedback_show/', client_views.feedback_show),
    path('search_product/',client_views.autosuggest,name='pro_search'),

]
