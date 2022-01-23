from django.urls import path
from bbank_client import client_views
import include

urlpatterns = [
    path('client_login/', views.login),
    path('forgot/', views.forgot),
    path('send_otp/', views.send_otp),
]