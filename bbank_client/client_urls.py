from django.urls import path
from bbank_client import client_views
import include

urlpatterns = [
    path('client_login/', client_views.login),
    path('forgot/', client_views.forgot),
    path('send_otp/', client_views.send_otp),
    path('set_password/', client_views.reset),
    path('home/', client_views.home),
    path('search_product/', client_views.autosuggest, name='pro_search'),
    path('search12/', client_views.search),
]