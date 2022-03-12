from django.db import models
import datetime

class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    area_name = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=6)

    class Meta:
        db_table = "bloodbank_area"


class Bloodbank(models.Model):
    b_id = models.AutoField(primary_key=True)
    b_name = models.CharField(max_length=50)
    b_address = models.CharField(max_length=300, null=False)
    b_img = models.FileField()
    b_email = models.EmailField(unique=True)
    b_pwd = models.CharField(max_length=15)
    b_contact = models.BigIntegerField()
    b_timing = models.TimeField()
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)
    description = models.CharField(max_length=100 , default="desc")


    class Meta:
        db_table = "bloodbank_bloodbank"


class Blood_grp(models.Model):
    bloodgrp_id = models.AutoField(primary_key=True)
    bloodgrp_type = models.CharField(max_length=5)
    bloodgrp_status = models.CharField(max_length=120 , default="0")

    class Meta:
        db_table = "bloodbank_bloods_grp"


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    bloodgrp_id = models.ForeignKey(Blood_grp, on_delete=models.CASCADE)
    Gender = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    dob = models.DateTimeField()
    user_weight = models.IntegerField()
    contact_no = models.BigIntegerField()
    id_proof = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=8)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)

    class Meta:
        db_table = "bloodbank_user"


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    e_name = models.CharField(max_length=100)
    e_date = models.DateField()
    b_id = models.ForeignKey(Bloodbank, on_delete=models.CASCADE)
    e_des = models.CharField(max_length=500)
    e_img = models.FileField()
    e_location = models.CharField(max_length=200)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)

    class Meta:
        db_table = "bloodbank_event"


class Blood_stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    bloodgrp_id = models.ForeignKey(Blood_grp, on_delete=models.CASCADE)
    b_stock = models.IntegerField()
    b_id = models.ForeignKey(Bloodbank, on_delete=models.CASCADE)

    class Meta:
        db_table = "bloodbank_bloodstock"


class Van(models.Model):
    van_id = models.AutoField(primary_key=True)
    van_num = models.IntegerField(null=False)
    v_datetime = models.DateTimeField()
    v_add = models.CharField(max_length=300)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = "bloodbank_van"


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    given_date = models.DateField()
    b_id = models.ForeignKey(Bloodbank, on_delete=models.CASCADE)
    appointment_status = models.CharField(max_length=20)
    appointment_time = models.DateTimeField()


    class Meta:
        db_table = "bloodbank_appointment"


class Gallery(models.Model):
    gallery_id = models.AutoField(primary_key=True)
    b_id = models.ForeignKey(Bloodbank, on_delete=models.CASCADE)
    img_path = models.FileField()
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        db_table = "bloodbank_gallery"


class Request_blood(models.Model):
    request_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bloodgrp_id = models.ForeignKey(Blood_grp, on_delete=models.CASCADE)
    b_id = models.ForeignKey(Bloodbank, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    qty = models.IntegerField()

    class Meta:
        db_table = "bloodbank_requestblood"


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_fname = models.CharField(max_length=100)
    admin_lname = models.CharField(max_length=50)
    admin_email = models.EmailField(unique=True)
    admin_contact = models.CharField(max_length=15)
    admin_password = models.CharField(max_length=15)
    admin_dob = models.DateField()
    admin_gender = models.CharField(max_length=7)
    otp = models.CharField(max_length=10, null=True)
    otp_used = models.IntegerField()
    is_admin = models.IntegerField()

    class Meta:
        db_table = "admin"


class Feedback(models.Model):
    f_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_b=models.CharField(max_length=200)
    f_date = models.DateTimeField()
    b_id = models.ForeignKey(Bloodbank, on_delete=models.CASCADE)
    ratings = models.IntegerField(default=5)

    class Meta:
        db_table = "bloodbank_feedback"


