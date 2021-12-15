""" Login, Register, Logout views """
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import redirect, render
from django.http import HttpResponse
from clubs.forms import RegisterForm, LogInForm, UserForm, PasswordForm, ClubForm
from clubs.models import User, Club
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

def unauthorised_access(request):
    """ unauthorised access to the website when a user is not logged in """
    return render(request, 'unauthorised_access.html')

def log_in(request):
    """ Log in request for an already registered user """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LogInForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, "Please Check Your Email And Password")

    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    """ Log out users who are logged into the website """
    logout(request)
    return redirect('log_in')

def register(request):
    """ User are who are not logged in are able to register a new account """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('log_in') #redirects to log_in after a valid form is completed
    else:
        form = RegisterForm()

    return render(request,'register.html', {'form':form})

@login_required
def password(request):
    """ Change the password of the current user """
    current_user = request.user
    if request.method == 'POST':
        form = PasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if check_password(password, current_user.password):
                new_password = form.cleaned_data.get('new_password')
                current_user.set_password(new_password)
                current_user.save()
                login(request, current_user)
                messages.add_message(request, messages.SUCCESS, "Password updated!")
                return redirect('home')
    form = PasswordForm()
    return render(request, 'password.html', {'form': form})
