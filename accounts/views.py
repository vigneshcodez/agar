from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages

User = get_user_model()

def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST.get("username")  
        password = request.POST.get("password")

        user = User.objects.create_user(username=username, email=email, password=password,is_active=False)  

        # Email Verification
        current_site = get_current_site(request)
        mail_subject = "Activate your account"
        message = render_to_string('accounts_templates/email_verification.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        email_message = EmailMessage(mail_subject, message, to=[email])
        email_message.send()

        messages.success(request, "Please confirm your email to complete registration.")
        return redirect("login")

    return render(request, "accounts_templates/register.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated!")
        return redirect("login")
    else:
        messages.error(request, "Invalid activation link.")
        return redirect("register")

from django.contrib.auth import authenticate, login, logout

def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials.")
    
    return render(request, "accounts_templates/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name="accounts_templates/password_reset_email.html",
            )
            messages.success(request, "Check your email for the reset link.")
            return redirect("login")
    else:
        form = PasswordResetForm()
    return render(request, "accounts_templates/password_reset.html", {"form": form})

def password_reset_confirm(request, uidb64, token):
    if request.method == "POST":
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password reset successful. You can now log in.")
            return redirect("login")
    else:
        form = SetPasswordForm(request.user)
    return render(request, "accounts_templates/password_reset_confirm.html", {"form": form})

