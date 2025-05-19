from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, models
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

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
