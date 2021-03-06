from django import forms
from bbank_admin.models import Area
from bbank_admin.models import Blood_grp
from bbank_admin.models import User
from bbank_admin.models import Bloodbank
from bbank_admin.models import Blood_stock
from bbank_admin.models import Appointment
from bbank_admin.models import Request_blood
from bbank_admin.models import Event
from bbank_admin.models import Gallery
from bbank_admin.models import Van
from bbank_admin.models import Feedback
from bbank_admin.models import Admin


# class UserForm(forms.ModelForm):
#   class Meta:
#      model = User
#     fields = ["u_id", "u_name", "u_email", "u_contact", "u_pwd", "otp", "otp_used", "area_id", "is_admin"]


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["area_name", "pincode"]


class Blood_grpForm(forms.ModelForm):
    class Meta:
        model = Blood_grp
        fields = ["bloodgrp_type"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "bloodgrp_id", "Gender", "email", "dob", "user_weight", "contact_no",
                  "id_proof", "address", "password", "area_id"]


class BbankForm(forms.ModelForm):
    class Meta:
        model = Bloodbank
        fields = ["b_name", "b_address", "b_email", "b_pwd", "b_img", "b_contact", "b_timing", "area_id"]


class Blood_stockForm(forms.ModelForm):
    class Meta:
        model = Blood_stock
        fields = ["bloodgrp_id", "qty", "b_id"]


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["u_id", "b_id", "given_date", "appointment_status", "appointment_time", "appointment_date"]


class Request_bloodForm(forms.ModelForm):
    class Meta:
        model = Request_blood
        fields = ["u_id", "bloodgrp_id", "b_id", "status", "qty"]


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['e_date', 'b_id', 'e_des', 'e_location', 'area_id', 'gallery_id']


class VanForm(forms.ModelForm):
    class Meta:
        model = Van
        fields = ["van_num", "v_datetime", "v_add", "area_id", "description"]


class GalleryForm(forms.ModelForm):
    img_path = forms.FileField()

    class Meta:
        model = Gallery
        fields = ["img_path", "b_id"]


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["u_id", "feedback_b", "f_date", "b_id"]


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ["admin_fname", "admin_lname", "admin_email", "admin_contact", "admin_dob", "admin_gender"]