from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, models
from django.contrib import messages

def login_view(request):

    if request.method == "POST":
        username = request.POST["username"]
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
                request.POST["password"] == "" or \
                request.POST["first_name"] == "" or \
                request.POST["last_name"] == "":
                messages.error(request, f"لطفاً همه فیلدها را پر کنید.")
            else:
                user = models.User.objects.create_user(
                    username=request.POST["email"],
                    password=request.POST["password"],
                    email=request.POST["email"],
                    first_name=request.POST["first_name"],
                    last_name=request.POST["last_name"],
                )
                user.save()
                
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
