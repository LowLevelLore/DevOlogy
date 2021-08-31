import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from DevOlogy.settings import WEBSITE_NAME, WEBSITE_DOMAIN, EMAIL_HOST_USER
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth import views as default_views
import threading
import json

# Create your views here.


def log_out_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    if request.method == "GET":
        logout(request)  # REMOVE AFTERWARDS
        pass


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        print(email)

        try:
            user = get_user_model().objects.get(email=email)

            subject = "Password Reset Requested"
            email_template_name = "text/password_reset_email.txt"
            c = {
                "email": user.email,
                "domain": WEBSITE_DOMAIN,
                "site_name": f"{WEBSITE_NAME}",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": default_token_generator.make_token(user),
                "protocol": "http",
                "username": user.username,
                "last": f"Team {WEBSITE_NAME} .",
            }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(
                    subject, email, EMAIL_HOST_USER, [user.email], fail_silently=False
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found.")  # Make a view for it
            return redirect("password_reset_done_view")
        except Exception as e:
            print(e)
            password_reset_form = PasswordResetForm()
            return render(
                request=request,
                template_name="auth/PasswordReset/password_reset.html",
                context={
                    "password_reset_form": password_reset_form,
                    "error": "Email not Registered",
                },
            )

    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="auth/PasswordReset/password_reset.html",
        context={"password_reset_form": password_reset_form},
    )


def login_view(request):
    if request.method == "POST":
        if request.is_ajax():
            if request.method == "POST":
                login_data = json.loads(request.body)
                username_email = login_data["username"]
                password = login_data["password"]
                try:
                    email = get_user_model().objects.get(username=username_email).email
                except:
                    email = username_email
                    user = authenticate(email=email, password=password)
                if user:
                    login(request, user)
                    isSuccessful = True
                else:
                    isSuccessful = False
                response = {"IsLoginSuccessful": isSuccessful}
                return HttpResponse(
                    json.dumps(response), content_type="application/json"
                )
        else:
            return HttpResponse("Page Not Found")
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return render(request, "frontend/index.html")
    else:
        pass  # Error 404 Page To Be Created


def sign_up_view(request):
    if request.method == "POST":
        pass
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return render(request, "frontend/index.html")
    else:
        pass  # Error 404 Page To Be Created
