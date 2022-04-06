from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, response
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from DevOlogy.settings import WEBSITE_NAME, EMAIL_HOST_USER
from django.contrib.auth import authenticate, login, logout, get_user_model
import json
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import email_confirmation_token
from django.core.mail import send_mail
from .models import InactiveUser
from django.views.decorators.csrf import ensure_csrf_cookie


USER_MODEL = get_user_model()
INACTIVE_USER_MODEL = InactiveUser


def fb_login_view(request):
    pass

@ensure_csrf_cookie
def log_out_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    if request.method == "GET":
        logout(request)  # REMOVE AFTERWARDS
        pass

@ensure_csrf_cookie
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
                "domain": get_current_site.domain,
                "site_name": f"{WEBSITE_NAME}",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": default_token_generator.make_token(user),
                "protocol": "https",
                "username": user.username,
                "last": f"Team {WEBSITE_NAME} .",
            }

            email = render_to_string(email_template_name, c)
            try:
                send_mail(
                    subject, email, EMAIL_HOST_USER, [
                        user.email], fail_silently=False
                )
            except BadHeaderError:
                # Make a view for it
                return HttpResponse("Invalid header found.")
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

@ensure_csrf_cookie
def login_view(request):
    if request.method == "POST":
        if request.is_ajax():
            login_data = json.loads(request.body)
            username_email = login_data["username"]
            password = login_data["password"]
            try:
                email = get_user_model().objects.get(username=username_email).email
            except:
                email = username_email
                user = authenticate(email=email, password=password)
                print(user)
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
        print("get")
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return render(request, "frontend/index.html")
    else:
        pass  # Error 404 Page To Be Created

@ensure_csrf_cookie
def sign_up_view(request):
    if request.method == "POST":
        if request.is_ajax():
            login_data = json.loads(request.body)
            email = login_data["email"]
            username = login_data["username"]
            name = login_data["name"]
            password = login_data["password"]
            rel = list(get_user_model().objects.prefetch_related().filter(email=email))
            if len(rel) == 0:
                user = INACTIVE_USER_MODEL.objects.create(email= email, username=username, full_name=name)
                user.save()
                current_site = get_current_site(request)
                request.session["password"] = password
                mail_subject = 'Activate your account.'
                
                message = render_to_string('html/email_template.html', {
                            'name': name,
                            'protocol': 'https',
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.custom_id)),
                            'token': email_confirmation_token.make_token(user),
                            "last": f"Team {WEBSITE_NAME} ."
                        })
                to_email = email
                
                message = EmailMessage(mail_subject, message, EMAIL_HOST_USER, [to_email])
                message.content_subtype = 'html' 
                message.send()
                
                msg = "Mail Sent To Email"
                code = 200
            else:
                msg = "Invalid Credentials"
                code = 401
            
            response = {"message": msg, "code": code}

            return HttpResponse(
                json.dumps(response), content_type="application/json"
            )
                
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return render(request, "frontend/index.html")
    else:
        pass  # Error 404 Page To Be Created


def user_data_deletion(request):
    pass

@ensure_csrf_cookie
def activate(request, uidb64, token):
    pass_ = request.session["password"]
    request.session["password"] = ""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = INACTIVE_USER_MODEL.objects.get(custom_id=uid)
        try_to_match = list(USER_MODEL.objects.filter(email= user.email))
        if email_confirmation_token.check_token(user, token):
            if len(try_to_match) == 0 :
                final_user = USER_MODEL.objects.create_user(username=user.username, email=user.email, full_name=user.full_name, password=pass_)
                final_user.save()
                user_ = authenticate(email=final_user.email, password=pass_)
                login(request, user_)
                user.delete()
                return redirect('/')
            else:
                return redirect('/login/')
        return HttpResponse("Please Try Again After Sometime .")
        
    except(TypeError, ValueError, OverflowError, INACTIVE_USER_MODEL.DoesNotExist):
        user = None
        return HttpResponse("Please Try Again After Sometime .")