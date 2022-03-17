from django.shortcuts import render, redirect
from bbank_admin.forms import UserForm
from bbank_admin.models import User, Bloodbank, Appointment, Admin
from bbank_admin.models import User, Bloodbank, Appointment, Blood_grp
import random
from bbank_admin.models import User, Bloodbank, Appointment, Blood_grp, Feedback
import random


def client_login(request):
    if request.method == "POST":
        d_email = request.POST.get("email")
        pas = request.POST.get("password")
        val = User.objects.filter(email=d_email, pas=password).count()
        print("------------------", d_email, "-----------------", pas)
        if val == 1:
            data = User.objects.filter(email=d_email, password=pas)
            for item in data:
                request.session['user_email'] = item.email
                request.session['user_pass'] = item.password
                request.session['user_id'] = item.d_id
                return redirect('/client/home/')
        else:
            messages.error(request, "Invalid user name and password")
            return redirect('/client/client_login')
    else:
        return render(request, "client_login.html")


def client_forgetpassword(request):
    return render(request, 'client_forgetpassword.html')


def client_sendotp(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST.get('email')

    request.session['temail'] = e
    print("===EMAILLLL===", e)
    obj = User.objects.filter(email=e).count()
    print("===OBJECTTTTTTT==", obj)
    if obj == 1:
        val = User.objects.filter(email=e).update(d_otp=otp1, d_otp_used=0)

        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)

    return render(request, 'client_setpassword.html')


def client_set_password(request):
    if request.method == "POST":

        T_otp = request.POST.get('d_otp')
        T_pass = request.POST.get('password')
        T_cpass = request.POST.get('cpass')

        if T_pass == T_cpass:
            print("=====PASSWORDDDDDDDDDDDDDDD=====", T_pass, T_cpass)
            e = request.session['temail']
            val = User.objects.filter(email=e, otp=T_otp, otp_used=0).count()
            print("===========", val)
            if val == 1:
                User.objects.filter(email=e).update(d_otp_used=1, password=T_pass)
                return redirect("/client_login/")
            else:
                messages.error(request, "Invalid OTP")
                return render(request, "client_forgetpassword.html")

        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "client_forgetpassword.html")

    else:
        return redirect("/client_forgetpassword")


def home(request):
    return render(request, "home.html")


def contact(request):
    return render(request, "contact.html")


def autosuggest(request):
    if 'term' in request.GET:
        qs = Bloodbank.objects.filter(bloodgrp_type__istartswith=request.GET.get('term'))

        names = list()

        for x in qs:
            names.append(x.bloodgrp_type)
        return JsonResponse(names, safe=False)
    return render(request, "client_header.html")


def search(request):
    if request.method == "POST":
        name = request.POST["bloodgrp_type"]
        p = Bloodbank.objects.filter(bloodgrp_type=name)

    else:
        p = Blood_grp.objects.all()

    return render(request, "bloodbank.html", {"p": p})


def bbank_directory(request):
    bb = Bloodbank.objects.all()
    return render(request, "bbank_directory.html", {"bb":bb})


def aboutus(request):
    return render(request, "about_us.html")


def appointment_details(request):
    return render(request, "appointment_details.html")


def gallery(request):
    return render(request, "gallery.html")


def client_register(request):
    bloodgroup = Blood_grp.objects.all()
    if request.method == "POST":
        form = UserForm(request.POST)
        print("-------------", form.errors)
        print("======", request.POST.get('is_admin'))
        if form.is_valid():
            try:
                form.save()
                return redirect('/client/client_login')
            except:
                print("---------------", sys.exc_info())
    else:
        form = UserForm()
    return render(request, 'registration.html', {'form': form, "bloodgroup": bloodgroup})


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


def client_update_profile(request):
    bloodgroup = Blood_grp.objects.all()
    a_id =Admin.objects.all()
    u = User.objects.get(email=a_id)
    form = UserForm(request.POST, instance=u)
    print("-------------", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/client/client_login/")
        except:
            print("---------------", sys.exc_info())
    else:
        pass
    return render(request, "client_profile.html", {'ca': u, "bloodgroup": bloodgroup})


def feedback_show(request):
    fb = FeedBack.objects.all()
    return render(request, "feedback_show.html", {'fb': fb})


def client_feedback(request):
    if request.method == "POST":
        try:
            description = request.POST['feedback_b']
            print("|||||||||||||",description)
            BloodBank = request.POST.get('b_id')
            print("|||||||||||||||||||||||||||||",BloodBank)
            User_id = request.session['d_id']
            f_date = date.today()
            rate = request.POST.get('rate')

            feed = FeedBack(User_id_id=User_id, b_id_id=BloodBank, feedback_b=description,
                            f_date=f_date, Ratings=rate)
            feed.save()
            return redirect("/client/client_bloodbankdetails/%s" % BloodBank)
        except:
            print("=======", sys.exc_info())
    else:
        pass
    return render(request, "client_bloodbankdetails.html")


def bloodbank_details(request, id):
    bb = Bloodbank.objects.get(b_id=id)
    feed = Feedback.objects.filter(b_id=id)  # Showing Feedbacks
    feed_count = Feedback.objects.filter(b_id=id).count()
    rate = 0
    for data in feed:
        rate += data.Ratings

    if feed_count > 0:
        count_rate = rate / feed_count
    else:
        count_rate = None
    return render(request, "client_bloodbankdetails.html",
                  {'bb': bb, 'feed': feed, 'f_count': feed_count, 'count_rate': count_rate,'blood_id':id})


def client_appointment(request, id):
    if request.method == "POST":
        try:
            u = request.session['d_id']
            dat = date.today().strftime("%Y-%m-%d")
            tim = request.POST['appointment_time']
            ddate = request.POST['donation_date']
            book = Appointment(u_id_id=Donor, b_id_id=id, given_date=dat, appointment_time=tim, donation_date=ddate, appointment_status=0)
            book = Appointment(u_id_id=u,b_id_id=id,given_date=dat, appointment_time=tim, donation_date=ddate, appointment_status=0)
            book.save()
            return redirect("/client/bbank_directory")
        except:
            print("---------------", sys.exc_info())

    return render(request, 'client_appointment.html', {'blood_id': id})



