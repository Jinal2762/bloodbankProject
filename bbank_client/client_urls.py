from django.urls import path
from bbank_client import client_views
import include


urlpatterns = [
    path('client_login/', client_views.login),
    path('forgot/', client_views.forgotc),
    path('send_otp/', client_views.send_otpc),
    path('set_password/', client_views.resetc),
    path('home/', client_views.home),
    path('bbank_details/', client_views.bbank_details),
    path('appointment_details/', client_views.appointment_details),
    path('bbank_directory/', client_views.bbank_directory),
    path('search_product/', client_views.autosuggest, name='pro_search'),
]

