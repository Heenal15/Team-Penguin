""" Display all the views that help to display different user """
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import redirect, render
from django.http import HttpResponse
from clubs.models import User
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from .user_type_check import *
from .authentication_views import *

@user_passes_test(is_club_owner_or_officer, login_url='unauthorised_access', redirect_field_name=None)
def applicant_list(request):
    """ Show all applicants list """
    applicants = User.objects.filter(user_type = 0)
    return render(request, 'applicant_list.html', {'applicants': applicants})

@user_passes_test(is_club_owner_or_officer_or_member, login_url='unauthorised_access', redirect_field_name=None)
def show_member(request, user_id):
    """ Show current user infromation """
    try:
        user = User.objects.get(id = user_id)
    except ObjectDoesNotExist:
        return redirect('member_list')
    else:
        return render(request, 'show_member.html', {'user': user})

@user_passes_test(is_club_owner_or_officer, login_url='unauthorised_access', redirect_field_name=None)
def show_user(request, user_id):
    """ Show a list of all users """
    try:
        user = User.objects.get(id = user_id)
    except ObjectDoesNotExist:
        #return redirect('full_user_list','memberlist_Clubowner')
        return redirect('home')
    else:
        return render(request, 'show_user.html', {'user': user})

# @user_passes_test(is_member, login_url='unauthorised_access', redirect_field_name=None)
# def member_list(request):
#     """ Show all members """
#     members = User.objects.filter(user_type = 1)
#     return render(request, 'member_list.html', {'members': members})
#
# @user_passes_test(is_club_officer, login_url='unauthorised_access', redirect_field_name=None)
# def member_list_for_officer(request):
#     """ Show all members to officers """
#     members = User.objects.filter(user_type = 1)
#     return render(request, 'member_list_for_officer.html', {'members': members})
#
# @user_passes_test(is_club_owner, login_url='unauthorised_access', redirect_field_name=None) #redirects unauthorised users
# def members_and_officers_for_clubowner(request):
#     """ Show all members and officers to club owners """
#     members = User.objects.filter(user_type = 1)
#     officers =  User.objects.filter(user_type = 2)
#     members_and_officers = members | officers
#     return render(request, 'members_and_officers_for_clubowner.html', {'members_and_officers': members_and_officers})

@user_passes_test(is_club_owner_or_officer_or_member, login_url='unauthorised_access', redirect_field_name=None) #redirects unauthorised users
def user_list(request):
    """ Show all members and officers to club owners """
    members = User.objects.filter(user_type = 1)
    officers =  User.objects.filter(user_type = 2)
    members_and_officers = members | officers
    return render(request, 'user_list.html', {'members_and_officers': members_and_officers, 'members': members})

@user_passes_test(is_club_owner, login_url='unauthorised_access', redirect_field_name=None)
def officers(request):
    """ Show all officers list """
    officers = User.objects.filter(user_type = 2)
    return render(request, 'officers.html', {'officers': officers})
