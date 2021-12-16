""" User types of a user can be changed and updated according to what is clicked on the webpage loaded """
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
from .user_type_check import *

@user_passes_test(is_club_owner_or_officer, login_url='unauthorised_access', redirect_field_name=None)
def approve(request, user_id):
    """ Approve a an applicant """
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 0:
        current_user.user_type = 1
        current_user.save()
    applicants = User.objects.filter(user_type = 0)
    return render(request, 'applicant_list.html', {'applicants': applicants})

@user_passes_test(is_club_owner_or_officer, login_url='unauthorised_access', redirect_field_name=None)
def unapprove(request, user_id):
    """ Unapprove an applicant """
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 0:
        current_user.delete()
    applicants = User.objects.filter(user_type = 0)
    return render(request, 'applicant_list.html', {'applicants': applicants})

@user_passes_test(is_club_owner, login_url='unauthorised_access', redirect_field_name=None)
def promote(request, user_id):
    """ Promote a user """
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 1:
        current_user.user_type = 2
        current_user.save()
    members = User.objects.filter(user_type = 1)
    officers =  User.objects.filter(user_type = 2)
    members_and_officers = members | officers
    return render(request, 'user_list.html', {'members_and_officers': members_and_officers})

@user_passes_test(is_club_owner, login_url='unauthorised_access', redirect_field_name=None)
def demote(request, user_id):
    """ Demote a user """
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 2:
        current_user.user_type = 1
        current_user.save()
    members = User.objects.filter(user_type = 1)
    officers =  User.objects.filter(user_type = 2)
    members_and_officers = members | officers
    return render(request, 'user_list.html', {'members_and_officers': members_and_officers})

@user_passes_test(is_club_owner, login_url='unauthorised_access', redirect_field_name=None)
def make_owner(request, user_id):
    """ Make some an owner """
    user = request.user
    current_user = User.objects.get(id = user_id)
    user.user_type = 2
    user.save()
    if User.objects.filter(user_type = 3).exists():
        officers = User.objects.filter(user_type = 2)
    else:
        current_user.user_type = 3
        current_user.save()
        officers = User.objects.filter(user_type = 2)
    return render(request, 'officers.html', {'officers': officers})
