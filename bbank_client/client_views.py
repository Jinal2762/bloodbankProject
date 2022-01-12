from django.shortcuts import render

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        val = Admin.objects.filter(admin_email=email, admin_password=password, is_admin=1).count()
        print("------------------", email, "-----------------", password)
        if val == 1:
            data = Admin.objects.filter(admin_email=email, admin_password=password, is_admin=1)
            for item in data:
                request.session['a_email'] = item.admin_email
                request.session['a_pw'] = item.admin_password
        else:
            messages.error(request, "Invalid user name and password")
            return redirect('/login')
    else:
        return render(request, "login.html")


def forgot(request):
    return render(request, 'passcode-reset.html')


def send_otp(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']

    request.session['temail'] = e

    obj = Admin.objects.filter(admin_email=e).count()

    if obj == 1:
        val = Admin.objects.filter(admin_email=e).update(otp=otp1, otp_used=0)

        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)

        return render(request, 'set_password.html')


def set_password(request):
    if request.method == "POST":

        T_otp = request.POST['otp']
        T_pass = request.POST['admin_password']
        T_cpass = request.POST['cpass']

        if T_pass == T_cpass:

            e = request.session['temail']
            val = Admin.objects.filter(admin_email=e, otp=T_otp, otp_used=0).count()

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