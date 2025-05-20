from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, models
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponse

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from .models import PasswordResetTracker

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('login')  # یا هر صفحه دلخواه بعد از موفقیت

    def dispatch(self, request, *args, **kwargs):
        self.user = self.get_user(kwargs['uidb64'])
        if self.user is None or not self.token_is_valid(self.user, kwargs['token']):
            return self.invalid_link_response()
        return super().dispatch(request, *args, **kwargs)

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    def token_is_valid(self, user, token):
        return default_token_generator.check_token(user, token)

    def invalid_link_response(self):
        return HttpResponse("این لینک دیگر معتبر نیست یا قبلاً استفاده شده است.", status=400)


def is_email(value):
    try:
        validate_email(value)
        return True
    except ValidationError:
        return False


def login_view(request):
    if request.method == "POST":        
        if request.POST["username_email"] == "" or request.POST["password"] == "":
            messages.error(request, f"لطفاً همه فیلدها را وارد کنید.")
            return render(request, 'accounts/signin.html')
        else:   
            username = ""
            if is_email(request.POST["username_email"]):
                username = User.objects.get(email=request.POST["username_email"]).username
            else:
                username = request.POST["username_email"]
        
        password = request.POST["password"]
        user = authenticate(request, username= username, password=password)
        
        if user is not None:
            login(request, user=user)
            return redirect("/blog")
        else:
            messages.error(request, f"نام کاربری یا رمز عبور اشتباه است.")
            #return redirect("/accounts/login")

    return render(request, 'accounts/signin.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/accounts/login')


def signup_view(request):
    try:
        if request.method == "POST":
            if  request.POST["email"] == "" or \
                request.POST["username"] == "" or \
                request.POST["password"] == "" or \
                request.POST["first_name"] == "" or \
                request.POST["last_name"] == "":
                messages.error(request, f"لطفاً همه فیلدها را پر کنید.")
                
            elif not User.objects.filter(email=request.POST["email"]).exists():
                user = models.User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password"],
                    email=request.POST["email"],
                    first_name=request.POST["first_name"],
                    last_name=request.POST["last_name"],
                )
                user.save()
                messages.add_message(request, messages.SUCCESS, f'ثبت نام شما با موفقیت انجام شد لطفاً از طریق فرم زیر وارد شوید.')
                return render(request, 'accounts/signin.html')
            
            else:
                messages.error(request, f"ایمیل وارد شده از قبل وجود دارد لطفاً یک آدرس ایمیل دیگر وارد کنید.")
                
    except Exception as e:
        if str(e) == "UNIQUE constraint failed: auth_user.username":
            messages.error(request, f"نام کاربری وارد شده وجود دارد. لطفاً یک نام کاربری دیگر وارد کنید.")
        else:
            messages.error(request, f"خطا در ثبت نام: {str(e)}")
            
    return render(request, 'accounts/signup.html')

def forgot_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    return render(request, "accounts/forgot.html")