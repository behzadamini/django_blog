from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, models

def login_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username= username, password=password)
        
        if user is not None:
            login(request, user=user)
            return redirect("/blog")
        else:
            return redirect("/accounts/login")

    return render(request, 'accounts/signin.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/accounts/login')


def signup_view(request):

    if request.method == "POST":
        user = models.User.objects.create_user(
            username=request.POST["email"],
            password=request.POST["password"],
            email=request.POST["email"],
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
        )
        user.save()
    return render(request, 'accounts/signup.html')

def forgot_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    return render(request, "accounts/forgot.html")
