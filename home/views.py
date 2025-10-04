from django.shortcuts import render, HttpResponse , redirect , get_object_or_404
from datetime import datetime
from home.models import Contact , EmergencyContact
from django.contrib import messages
from django.contrib.auth.models  import User
from django.contrib.auth import logout, authenticate , login
#new
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json
from home.utils import send_sms, send_whatsapp

def loginuser(request):
    if request.method == "POST":
        #check user has entered correct credentials
        username=request.POST.get('username')
        #email=request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(username=username , password=password)
        if user is not None: #authenticate user 
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('/login')
            
         
    return render(request,'login.html') # username=Himanshi pwd=Mywebsite123
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, "login.html", {"open_signup": True})

        # Username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, "login.html", {"open_signup": True})

        # Email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, "login.html", {"open_signup": True})

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return redirect("login")


def logoutuser(request):
    logout(request)
    return redirect('/login')

def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'data.html')
def sos(request):
    if request.user.is_anonymous:
        return redirect("/login")
    #new
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone_number')
        email = request.POST.get('email')
        EmergencyContact.objects.create(user=request.user , name=name, phone_number=phone, email=email)
        return redirect('sos')

    contacts = EmergencyContact.objects.filter(user=request.user)
    return render(request,'sos.html', {"contacts": contacts})
def live(request):
    if request.user.is_anonymous:
        return redirect("/login")
    #new
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone_number')
        email = request.POST.get('email')
        EmergencyContact.objects.create(user=request.user , name=name, phone_number=phone, email=email)
        return redirect('live')

    contacts = EmergencyContact.objects.filter(user=request.user)
    return render(request,'live.html', {"contacts": contacts})
@csrf_exempt
@login_required
def send_alert(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lat = data.get("latitude")
            lon = data.get("longitude")
            location_link = f"https://www.google.com/maps?q={lat},{lon}"

            contacts = EmergencyContact.objects.filter(user=request.user)

            for contact in contacts:
                alert_message = (
                    f"🚨 Emergency Alert from your contact {request.user.username}! \n  This is an emergency! I feel unsafe and need help right now. Please contact me immediately.\n"
                    f"Track my Live Location: {location_link}"
                )
                sms_message = (
                    f"EMERGENCY ALERT 🚨 {request.user.username} is unsafe. Immediate help needed.\n"
                    f" Location: {location_link}"

                )

                # 1. Email
                if contact.email:
                    send_mail(
                        subject="Emergency Alert from HerHeaven",
                        message= alert_message ,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[contact.email],
                        fail_silently=False
                    )
                 # 2. SMS
                if contact.phone_number:
                    try:
                        send_sms(
                            contact.phone_number, sms_message
                            )
                    except Exception as sms_error:
                        print(f"SMS failed: {sms_error}")
                    

                # 3. WhatsApp
                if contact.phone_number:
                    try:
                        send_whatsapp(
                            contact.phone_number, alert_message
                            )
                    except Exception as wa_error:
                        print(f"WhatsApp failed: {wa_error}")

            return JsonResponse({"status": True})
        except Exception as e:
            return JsonResponse({"status": False, "error": str(e)})

    return JsonResponse({"status": False, "error": "Invalid request"})
@csrf_exempt
@login_required
def send_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lat = data.get("latitude")
            lon = data.get("longitude")
            location_link = f"https://www.google.com/maps?q={lat},{lon}"

            contacts = EmergencyContact.objects.filter(user=request.user)

            for contact in contacts:
                alert_message = (
                    f"🚨 Live location from your contact {request.user.username}! \n I’m not sure, but I have a feeling something isn’t right. Please stay alert and keep an eye on me.!\n"  
                    f"Here's my current Location: {location_link}"
                )
                sms_message = (
                    f"PRECAUTIOUS ALERT 🚨 from {request.user.username}.Please keep an eye on me !\n"
                    f"Location: {location_link}"
                )


                # 1. Email
                if contact.email:
                    send_mail(
                        subject="Emergency Alert from HerHeaven",
                        message= alert_message ,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[contact.email],
                        fail_silently=False
                    )
                 # 2. SMS
                if contact.phone_number:
                    try:
                        send_sms(
                            contact.phone_number, sms_message
                            )
                    except Exception as sms_error:
                        print(f"SMS failed: {sms_error}")

                # 3. WhatsApp
                if contact.phone_number:
                    try:
                        send_whatsapp(
                            contact.phone_number, alert_message
                            )
                    except Exception as wa_error:
                        print(f"WhatsApp failed: {wa_error}")

            return JsonResponse({"status": True})
        except Exception as e:
            return JsonResponse({"status": False, "error": str(e)})

    return JsonResponse({"status": False, "error": "Invalid request"})
@login_required
def delete_contact(request, pk , source):
    contact = get_object_or_404(EmergencyContact, id=pk, user=request.user)
    contact.delete()
    return redirect(source)

@login_required
def edit_contact(request, pk , source ):
    contact = get_object_or_404(EmergencyContact, id=pk, user=request.user)
    if request.method == "POST":
        contact.name = request.POST.get("name")
        contact.phone_number = request.POST.get("phone_number")
        contact.email = request.POST.get("email")
        contact.save()
        return redirect(source)
    return render(request, "edit_contact.html", {"contact": contact , "source":source})

def selfdefence(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'selfdefence.html')
def contact(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        cont=Contact(name=name,email= email ,message=message,date=datetime.today())
        cont.save()
        messages.success(request, 'Thank You!! Your message have been sent ')
        #return render(request,'data.html')
    return render(request,'data.html')

