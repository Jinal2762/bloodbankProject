"""Bloodbank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from bbank_admin import views
from django.urls import re_path as url
from bbank_admin.views import HomeView, ProjectChart
from bbank_client import client_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('send_otp/', views.send_otp),
    path('passcode-reset/', views.forgot),
    path('show_area/', views.show_area),
    path('area_form/', views.insert_area),
    path('delete/<int:area_id>', views.destroy_area),
    path('edit_area/<int:id>', views.edit_area),
    path('bloodgrp_form/', views.insert_bloodgrp),
    path('edit_bgrp/<int:id>', views.edit_bgrp),
    path('user_form/', views.insert_user),
    path('delete_bgrp/<int:bloodgrp_id>', views.destroy_bloodgrp),
    path('delete_appon/<int:appointment_id>', views.destroy_appointment),
    path('bloodstock_form/', views.insert_stock),
    path('edit_stock/<int:id>', views.edit_stock),
    path('bloodrequest_form/', views.insert_bloodrequest),
    path('edit_request/<int:id>', views.edit_request),
    path('events_form/', views.insert_event),
    path('gallery_form/', views.insert_gallery),
    path('vanscheduling_form/', views.insert_van),
    path('edit_van/<int:id>', views.edit_van),
    path('gallerequest_form/', views.insert_bloodrequest),
    path('delete_stock/<int:stock_id>', views.destroy_stock),
    path('show_bgrp/', views.show_bgrp),
    path('show_user/', views.show_user),
    path('edit_user/<int:id>', views.edit_user),
    path('show_bbank/', views.show_bbank),
    path('bbank_form/', views.insert_bbank),
    path('edit_bbank/<int:id>', views.edit_bbank),
    path('delete_bbank/<int:b_id>', views.destroy_bbank),
    path('edit_event/<int:id>', views.edit_event),
    path('edit_gallery/<int:id>', views.edit_gallery),
    path('edit_appointment/<int:id>', views.edit_appointment),
    path('show_stock/', views.show_stock),
    path('show_appointment/', views.show_appointment_show),
    path('appointment_form/', views.insert_appointment),
    path('show_requestblood/', views.show_requestblood),
    path('show_events/', views.show_events),
    path('show_van/', views.show_van),
    path('show_gallery/', views.show_gallery),
    path('show_feedback/', views.show_feedback),
    path('delete_stock/<int:stock_id>', views.destroy_stock),
    path('delete_feedback/<int:f_id>', views.destroy_feedback),
    path('delete_gallery/<int:gallery_id>', views.destroy_gallery),
    path('delete_req/<int:request_id>', views.destroy_request),
    path('delete_user/<int:d_id>', views.destroy_user),
    path('delete_event/<int:event_id>', views.destroy_events),
    path('delete_van/<int:van_id>', views.destroy_van),
    path('dashboard/', views.index),
    path('reset/', views.reset),
    path('edit_profile/', views.edit_admin_profile),
    url(r'charthome', HomeView.as_view(), name='home'),
    url(r'^api/chart/data/$', ProjectChart.as_view(), name="api-data"),
    path('client/', include('bbank_client.client_urls')),
]
