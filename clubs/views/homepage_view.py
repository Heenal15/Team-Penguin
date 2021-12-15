""" File to display the correct render of a a logged in user """
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


def homepage(request):
    """ Render homepage for all visitors to the site """
    return render(request, 'homepage.html')

@login_required
def dashboard(request):
    """ Once a user is logged in they will be able to access the main dashboard"""
    return render(request, 'dashboard.html')

@login_required
def profile(request):
    """ Display a user profile and allow to be updated accordingly """
    current_user = request.user
    if request.method == 'POST':
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('profile')
    else:
        form = UserForm(instance=current_user)
    return render(request, 'profile.html', {'form': form})
