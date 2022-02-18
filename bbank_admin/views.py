from django.shortcuts import render, redirect
from bbank_admin.function import handle_uploded_file
from bbank_admin.forms import AdminForm, AreaForm, VanForm, Blood_grpForm, BbankForm, UserForm, FeedbackForm, Blood_stockForm, AppointmentForm, Request_bloodForm, EventForm, GalleryForm
from bbank_admin.models import Area, Blood_grp, Bloodbank, Feedback, Blood_stock, User, Appointment, Request_blood, Admin, Event, Gallery, Van
import random
import sys
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import View


def show_area(request):
    area = Area.objects.all()
    return render(request, "show_area.html", {'areas': area})


def show_bgrp(request):
    bgrp = Blood_grp.objects.all()
    return render(request, "show_bgrp.html", {'bgrps': bgrp})


def show_user(request):
    user = User.objects.all()
    return render(request, "show_user.html", {'users': user})


def show_bbank(request):
    bbank = Bloodbank.objects.all()
    return render(request, "show_bbank.html", {'bbanks': bbank})


def show_stock(request):
    stock = Blood_stock.objects.all()
    return render(request, "show_stock.html", {'stocks': stock})


def show_appointment_show(request):
    a = Appointment.objects.all()
    print("=========INSIDE FUNCRION", a)
    return render(request, "show_appointment.html", {'a': a})


def show_requestblood(request):
    request_blood = Request_blood.objects.all()
    return render(request, "show_requestblood.html", {'request_bloods': request_blood})


def show_events(request):
    event = Event.objects.all()
    return render(request, "show_events.html", {'events': event})


def show_van(request):
    van = Van.objects.all()
    return render(request, "show_van.html", {'vans': van})


def show_gallery(request):
    gallery = Gallery.objects.all()
    return render(request, "show_gallery.html", {"gallerys": gallery})


def show_feedback(request):
    feedback = Feedback.objects.all()
    return render(request, "show_feedback.html", {"feedbacks": feedback})


def login(request):
    if request.method == "POST":

        email = request.POST.get("admin_email")
        password = request.POST.get("admin_password")
        val = Admin.objects.filter(admin_email=email, admin_password=password, is_admin=1).count()
        print("------------------", email, "-----------------", password)
        if val == 1:
            data = Admin.objects.filter(admin_email=email, admin_password=password, is_admin=1)
            for item in data:
                request.session['a_email'] = item.admin_email
                request.session['a_pw'] = item.admin_password
                request.session['a_id'] = item.admin_id
                return redirect('/dashboard/')
        else:
            messages.error(request, "Invalid user name and password")
            return redirect('/login')
    else:
        return render(request, "login.html")


def forgot(request):
    return render(request, 'passcode-reset.html')


def send_otp(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST.get('admin_email')

    request.session['temail'] = e
    print("===EMAILLLL===", e)
    obj = Admin.objects.filter(admin_email=e).count()
    print("===OBJECTTTTTTT==", obj)
    if obj == 1:
        val = Admin.objects.filter(admin_email=e).update(otp=otp1, otp_used=0)

        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)

    return render(request, 'set_password.html')


def reset(request):
    if request.method == "POST":

        T_otp = request.POST.get('otp')
        T_pass = request.POST.get('admin_password')
        T_cpass = request.POST.get('cpass')

        if T_pass == T_cpass:
            print("=====PASSWORDDDDDDDDDDDDDDD=====", T_pass, T_cpass)
            e = request.session['temail']
            val = Admin.objects.filter(admin_email=e, otp=T_otp, otp_used=0).count()
            print("===========", val)
            if val == 1:
                Admin.objects.filter(admin_email=e).update(otp_used=1, admin_password=T_pass)
                return redirect("/login")
            else:
                messages.error(request, "Invalid OTP")
                return render(request, "passcode-reset.html")

        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "set_password.html")

    else:
        return redirect("/passcode-reset")


def index(request):
    user = User.objects.filter().count()
    bb = Bloodbank.objects.filter().count()
    return render(request, "dashboard.html", {'user':user , 'bb': bb })


def edit_admin_profile(request):
    email = request.session['a_email']
    password = request.session['a_pw']
    id = request.session['a_id']
    admins = Admin.objects.get(admin_id=id)
    dob = admins.admin_dob
    print("=========", dob)

    dob = dob.strftime('%Y-%m-%d')
    if request.method == 'POST':

        val = Admin.objects.filter(admin_email=email, admin_password=password, admin_id=id).count()
        print("======", val)
        if val == 1:
            admins = Admin.objects.get(admin_id=id)
            form = AdminForm(request.POST, instance=admins)
            print("---------", form.errors)
            if form.is_valid():
                form.save()
                return redirect('/dashboard')
    return render(request, "edit_profile.html", {'details': admins, 'dob': dob})


def insert_area(request):
    if request.method == "POST":
        form = AreaForm(request.POST)
        print("----------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show_area')
            except:
                print("---------", sys.exc_info())
    else:
        form = AreaForm()
    return render(request, 'area_form.html', {'form': form})


def edit_area(request, id):
    area = Area.objects.get(area_id=id)
    if request.method == "POST":
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect("/show_area")
    return render(request, 'edit_area.html', {'area': area})


def destroy_area(request, area_id):
    area = Area.objects.get(area_id=area_id)
    area.delete()
    return redirect("/show_area")


def insert_appointment(request):
    temp = User.objects.all()
    flag = Bloodbank.objects.all()
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        print("-----5555------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show_appointment')
            except:
                print("----4444------", sys.exc_info())
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form, 'flag': flag, 'temp': temp})


def edit_appointment(request, id):
    flag = User.objects.all()
    temp = Bloodbank.objects.all()
    appointment = Appointment.objects.get(appointment_id=id)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("/show_appointment")
    return render(request, 'edit_appointment.html', {'appointment': appointment, 'flag': flag, 'temp': temp})


def destroy_appointment(request, appointment_id):
    appointment = Appointment.objects.get(appointment_id=appointment_id)
    appointment.delete()
    return redirect("/show_appointment")


def insert_bbank(request):
    print("====INSIDE FUNCTION====")
    temp = Area.objects.all()
    if request.method == "POST":
        form = BbankForm(request.POST, request.FILES)
        print("-----**********------", form.errors)
        if form.is_valid():
            try:
                handle_uploded_file(request.FILES['b_img'])
                form.save()
                return redirect('/show_bbank/')
            except:
                print("---hello-------", sys.exc_info())
    else:
        form = BbankForm()
    return render(request, 'bbank_form.html', {'form': form, 'temp': temp})


def edit_bbank(request, id):
    temp = Area.objects.all()
    bbank = Bloodbank.objects.get(b_id=id)
    if request.method == "POST":
        form = BbankForm(request.POST, instance=bbank)
        print("----------", form.errors)
        if form.is_valid():
            form.save()
            print("---------", sys.exc_info())
            return redirect("/show_bbank")
    return render(request, "edit_bbank.html", {'bbank': bbank, 'temp': temp})


def destroy_bbank(request, b_id):
    bbank = Bloodbank.objects.get(b_id=b_id)
    bbank.delete()
    return redirect("/show_bbank")


def insert_bloodgrp(request):
    if request.method == "POST":
        form = Blood_grpForm(request.POST)
        print("----------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show_bgrp')
            except:
                print("---------", sys.exc_info())
    else:
        form = Blood_grpForm()
    return render(request, 'bloodgrp_form.html', {'form': form})


def edit_bgrp(request, id):
    bgrp = Blood_grp.objects.get(bloodgrp_id=id)
    if request.method == "POST":
        form = Blood_grpForm(request.POST, instance=bgrp)
        if form.is_valid():
            form.save()
            return redirect("/show_bgrp")
    return render(request, "edit_bgrp.html", {'bgrp': bgrp, 'bgrp': bgrp})


def destroy_bloodgrp(request, bloodgrp_id):
    bgrp = Blood_grp.objects.get(bloodgrp_id=bloodgrp_id)
    bgrp.delete()
    return redirect("/show_bgrp")


def insert_stock(request):
    temp = Blood_grp.objects.all()
    flag = Bloodbank.objects.all()
    if request.method == "POST":
        form = Blood_stockForm(request.POST)
        print("----jjjj------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show_stock')
            except:
                print("---------", sys.exc_info())
    else:
        form = Blood_stockForm()
    return render(request, 'bloodstock_form.html', {'form': form, 'temp': temp, 'b': flag})


def edit_stock(request, id):
    temp = Blood_grp.objects.all()
    flag = Bloodbank.objects.all()
    stock = Blood_stock.objects.get(stock_id=id)
    if request.method == "POST":
        form = Blood_stockForm(request.POST, instance=stock)
        print("-----888888-----", form.errors)
        if form.is_valid():
            form.save()
            print("---------", sys.exc_info())
            return redirect("/show_stock")
    return render(request, "edit_stock.html", {'stock': stock, "b": flag, 'temp': temp})


def destroy_stock(request, stock_id):
    stock = Blood_stock.objects.get(stock_id=stock_id)
    stock.delete()
    return redirect("/show_stock")


def insert_bloodrequest(request):
    flag = Bloodbank.objects.all()
    temp1 = User.objects.all()
    temp2 = Blood_grp.objects.all()
    if request.method == "POST":
        form = Request_bloodForm(request.POST)
        print("-----------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show_requestblood')
            except:
                print("----------", sys.exc_info())
    else:
        form = Request_bloodForm()
    return render(request, 'bloodrequest_form.html',
                  {'form': form, 'flag': flag, 'temp1': temp1, 'temp2': temp2})


def edit_request(request, id):
    flag = Bloodbank.objects.all()
    temp1 = User.objects.all()
    temp2 = Blood_grp.objects.all()
    b_request = Request_blood.objects.get(request_id=id)
    if request.method == "POST":
        form = Request_bloodForm(request.POST, instance=b_request)
        if form.is_valid():
            form.save()
            return redirect("/show_requestblood")
    return render(request, "edit_request.html",
                  {'b_request': b_request, 'flag': flag, 'temp1': temp1, 'temp2': temp2})


def destroy_request(request, request_id):
    request = Request_blood.objects.get(request_id=request_id)
    request.delete()
    return redirect("/show_requestblood")


def insert_van(request):
    flag = Area.objects.all()
    if request.method == "POST":
        form = VanForm(request.POST)
        print("-----------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show_van')
            except:
                print("----------", sys.exc_info())
    else:
        form = VanForm()
    return render(request, 'vanscheduling_form.html', {'form': form, 'flag': flag})


def edit_van(request, id):
    flag = Area.objects.all()
    van = Van.objects.get(van_id=id)
    if request.method == "POST":
        form = VanForm(request.POST, instance=van)
        if form.is_valid():
            form.save()
            return redirect("/show_van")
    return render(request, "edit_van.html", {'van': van, 'flag': flag})


def destroy_van(request, van_id):
    van = Van.objects.get(van_id=van_id)
    van.delete()
    return redirect("/show_van")


def select_feedback(request, id):
    feedback = Feedback.objects.get(f_id=id)
    return render(request, 'edit_feedback.html', {'feedback': feedback})


def destroy_feedback(request, f_id):
    feedback = Feedback.objects.get(f_id=f_id)
    feedback.delete()
    return redirect("/show_feedback")


def insert_gallery(request):
    print("====INSIDE FUNCTION====")
    flag = Bloodbank.objects.all()
    print("========", flag)
    temp2 = Event.objects.all()
    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES)
        print("--+++++++++++++**---------", form.errors)
        if form.is_valid():
            try:
                handle_uploded_file(request.FILES['img_path'])
                form.save()
                return redirect('/show_gallery/')
            except:
                print("-----*********-----", sys.exc_info())
    else:
        form = GalleryForm()
    return render(request, 'gallery_form.html', {'form': form, 'flag': flag,'temp2': temp2})


def edit_gallery(request, id):
    flag = Bloodbank.objects.all()
    temp2 = Event.objects.all()
    gallery = Gallery.objects.get(gallery_id=id)
    if request.method == "POST":
        form = GalleryForm(request.POST, instance=gallery)
        if form.is_valid():
            form.save()
            return redirect("/show_gallery")
    return render(request, "edit_gallery.html", {'gallery': gallery, 'flag': flag, 'temp': temp, 'temp2': temp2})


def destroy_gallery(request, gallery_id):
    gallery = Gallery.objects.get(gallery_id=gallery_id)
    gallery.delete()
    return redirect("/show_gallery")


def insert_user(request):
    flag = Area.objects.all()
    temp = Blood_grp.objects.all()
    if request.method == "POST":
        form = UserForm(request.POST)
        print("-----88------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show_user')
            except:
                print("-----99-----", sys.exc_info())
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form, 'flag': flag, 'temp': temp})


def edit_user(request, id):
    flag = Area.objects.all()
    temp = Blood_grp.objects.all()
    user = User.objects.get(u_id=id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        print('9===========', form.errors)
        if form.is_valid():
            form.save()
            print('------------', sys.exc_info())
            return redirect("/show_user")
    return render(request, "edit_user.html", {'user': user, 'flag': flag, 'temp': temp})


def destroy_user(request, u_id):
    user = User.objects.get(u_id=u_id)
    user.delete()
    return redirect("/show_user")


def insert_event(request):
    flag = Bloodbank.objects.all()
    temp = Area.objects.all()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        print("-----------", request.POST.get('e_img'))
        print("-----------", form.errors)
        if form.is_valid():
            try:
                print("=========", request.FILES['e_img'])
                handle_uploded_file(request.FILES['e_img'])
                form.save()
                return redirect('/show_events')
            except:
                print("----------", sys.exc_info())
    else:
        form = EventForm()
    return render(request, 'events_form.html', {'form': form, 'flag': flag, 'temp': temp})


def edit_event(request, id):
    flag = Bloodbank.objects.all()
    temp = Area.objects.all()
    event = Event.objects.get(event_id=id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("/show_events")
    return render(request, "edit_event.html", {'event': event, 'flag': flag, 'temp': temp})


def destroy_events(request, event_id):
    event = Event.objects.get(event_id=event_id)
    event.delete()
    return redirect("/show_events")


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard.html")


class ProjectChart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        cursor = connection.cursor()
        cursor.execute(
            '''SELECT * from bloodbank_area''')
        qs = cursor.fetchall()
        print("=====0", qs)
        labels = []
        default_items = []
        for item in qs:
            labels.append(item[0])
            default_items.append(item[1])
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)

def accept_appointment(request,id):
    a = Appointment.objects.get(appointment_id=id)
    a.appointment_status='1'
    a.save()

    name=a.u_id.first_name
    print('love you',name)
    e=a.u_id.email
    subject="appointment accpeted"
    message="hey"+" "+name+",your appointment has been accepted"
    email_from=settings.EMAIL_HOST_USER
    recepient_list=[e, ]
    send_mail(subject,message,email_from,recepient_list)
    return redirect("/show_appointment")


def reject_appointment(request,id):
    a = Appointment.objects.get(appointment_id=id)
    a.appointment_status = '2'
    a.save()

    name = a.u_id.first_name
    print('love you', name)
    e = a.u_id.email
    subject = "appointment rejected"
    message = "hey" + " " + name + ",your appointment has been rejected"
    email_from = settings.EMAIL_HOST_USER
    recepient_list = [e, ]
    send_mail(subject, message, email_from, recepient_list)
    return redirect("/show_appointment")
