from django.shortcuts import render, redirect
from bbank_admin.forms import DonorForm
from bbank_admin.models import Donor,Bloodbank


def login(request):
    if request.method == "POST":
        d_email = request.POST.get("email")
        pas = request.POST.get("password")
        val = Donor.objects.filter(email=d_email, pas=password).count()
        print("------------------", d_email, "-----------------", pas)
        if val == 1:
            data = Donor.objects.filter(email=d_email, password=pas)
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


def forgotc(request):
    return render(request, 'forgot.html')


def send_otpc(request):
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


def resetc(request):
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


def home(request):
    return render(request, "home.html")


def autosuggest(request):
    if 'term' in request.GET:
        qs = Bloodbank.objects.filter(b_name__istartswith=request.GET.get('term'))

        names = list()

        for x in qs:
            names.append(x.b_name)
        return JsonResponse(names, safe=False)
    return render(request, "client_header.html")


def search(request):
    if request.method == "POST":
        name = request.POST["b_name"]
        p = Bloodbank.objects.filter(b_name=name)

    else:
        p = Bloodbank.objects.all()

    return render(request, "bloodbank.html", {"p": p})

