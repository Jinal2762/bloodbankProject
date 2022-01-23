from django.shortcuts import render, redirect
from bbank_admin import DonorForm,
from bbank_admin.models import Donor,


def login(request):
    if request.method == "POST":
        d_email = request.POST.get("email")
        pass = request.POST.get("password")
        val = Donor.objects.filter(email=d_email, pass=password).count()
        print("------------------", d_email, "-----------------", pass)
        if val == 1:
            data = Donor.objects.filter(email=d_email, password=pass)
            for item in data:
                request.session['donor_email'] = item.email
                request.session['donor_pass'] = item.password
                request.session['donor_id'] = item.d_id
                return redirect('/home/')
        else:
            messages.error(request, "Invalid user name and password")
            return redirect('/client_login')
    else:
        return render(request, "client_login.html")


def forgot(request):
    return render(request, 'passcode-reset.html')


def send_otp(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST.get('email')

    request.session['temail'] = e
    print("===EMAILLLL===", e)
    obj = Donor.objects.filter(admin_email=e).count()
    print("===OBJECTTTTTTT==", obj)
    if obj == 1:
        val = Donor.objects.filter(email=e).update(d_otp=otp1, d_otp_used=0)

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
            val = Donor.objects.filter(email=e, otp=T_otp, otp_used=0).count()
            print("===========", val)
            if val == 1:
                Donor.objects.filter(email=e).update(d_otp_used=1, password=T_pass)
                return redirect("/client_login")
            else:
                messages.error(request, "Invalid OTP")
                return render(request, "forgot.html")

        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "set_password.html")

    else:
        return redirect("/forgot")