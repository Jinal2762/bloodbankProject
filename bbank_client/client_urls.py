from django.urls import path
from bbank_client import client_views
import include


urlpatterns = [
    path('client_login/', client_views.login),
    path('forgot/', client_views.forgot),
    path('send_otp/', client_views.sendotp),
    path('reset/', client_views.reset),
    path('about_us/', client_views.aboutus),
    path('home/', client_views.home),
    path('appointment_details/', client_views.appointment_details),
    path('bbank_directory/', client_views.bbank_directory),
    path('search_product/', client_views.autosuggest, name='pro_search'),
    path('search12/', client_views.search),
    path('appointment_details/', client_views.appointment_details),
    path('registration/', client_views.client_register),
    path('aboutus/', client_views.aboutus),
    path('availability/', client_views.blood_availability),
    path('b_donate/', client_views.blood_donate),
    path('contact/', client_views.contact),
    path('events/', client_views.events),
    path('van_schedule/', client_views.van_schedule),
    path('b_request/', client_views.blood_request),
    path('gallery/', client_views.gallery),
    path('BB1/',client_views.bb_j),
    path('BB2/',client_views.bb_d),
    path('BB3/',client_views.bb_p),
    path('appointment_details/',client_views.appointment_details)

]
