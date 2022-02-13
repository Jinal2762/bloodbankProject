from django.shortcuts import render, redirect
from bbank_admin.forms import UserForm
from bbank_admin.models import User,Bloodbank


def login(request):
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
                return redirect('/home/')
        else:
            messages.error(request, "Invalid user name and password")
            return redirect('/client_login')
    else:
        return render(request, "client_login.html")


def forgot(request):
    return render(request, 'forgot.html')


def send_otp(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST.get('email')

    request.session['temail'] = e
    print("===EMAILLLL===", e)
    obj = User.objects.filter(admin_email=e).count()
    print("===OBJECTTTTTTT==", obj)
    if obj == 1:
        val = User.objects.filter(email=e).update(d_otp=otp1, d_otp_used=0)

        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)

    return render(request, 'set_password.html')


def reset(request):
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
                return redirect("/client_login")
            else:
                messages.error(request, "Invalid OTP")
                return render(request, "forgot.html")

        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "set_password.html")

    else:
        return redirect("/forgot")


def home(request):
    return render(request, "home.html")


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


def bbank_details(request):
    return render(request, "bbank-details.html")

