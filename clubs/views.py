from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import ApplicationForm, LogInForm, UserForm, PasswordForm
from .models import User
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                if user.user_type == 0:
                    return redirect('waiting_list')
                elif user.user_type == 1:
                    return redirect('members')
                elif user.user_type == 2:
                    return redirect('member_list_for_officer')
                elif user.user_type == 3:
                    return redirect('members_and_officers_for_clubowner')
                ## else:
                ##    return redirect('home')

        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('log_in') #redirects to log_in after a valid form is completed
    else:
        form = ApplicationForm()
    return render(request,'register.html', {'form':form})

#used to check if current user has privaleges to view page
def is_member(user):
    return (user.user_type == 1)

def is_club_officer(user):
    return (user.user_type == 2)

def is_club_owner(user):
    return (user.user_type == 3)

def unauthorised_access(request):
    return render(request, 'unauthorised_access.html')

@user_passes_test(is_club_owner, login_url='unauthorised_access', redirect_field_name=None) #redirects unauthorised users
def members_and_officers_for_clubowner(request):
    members = User.objects.filter(user_type = 1)
    officers =  User.objects.filter(user_type = 2)
    members_and_officers = members | officers
    return render(request, 'members_and_officers_for_clubowner.html', {'members_and_officers': members_and_officers})

@user_passes_test(is_club_officer, login_url='unauthorised_access', redirect_field_name=None)
def member_list_for_officer(request):
    members = User.objects.filter(user_type = 1)
    return render(request, 'member_list_for_officer.html', {'members': members})

@user_passes_test(is_member, login_url='unauthorised_access', redirect_field_name=None)
def member_list(request):
    members = User.objects.filter(user_type = 1)
    return render(request, 'member_list.html', {'members': members})

@user_passes_test(is_club_officer or is_club_owner, login_url='unauthorised_access', redirect_field_name=None)
def applicant_list(request):
    applicants = User.objects.filter(user_type = 0)
    return render(request, 'applicant_list.html', {'applicants': applicants})

def show_user(request, user_id):
    try:
        user = User.objects.get(id = user_id)
    except ObjectDoesNotExist:
        return redirect('home')
    else:
        return render(request, 'show_user.html', {'user': user})

def show_member(request, user_id):
    try:
        user = User.objects.get(id = user_id)
    except ObjectDoesNotExist:
        return redirect('member_list')
    else:
        return render(request, 'show_member.html', {'user': user})

def approve(request, user_id):
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 0:
        current_user.user_type = 1
        current_user.save()
    applicants = User.objects.filter(user_type = 0)
    return render(request, 'applicant_list.html', {'applicants': applicants})

def unapprove(request, user_id):
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 0:
        current_user.delete()
    applicants = User.objects.filter(user_type = 0)
    return render(request, 'applicant_list.html', {'applicants': applicants})

def promote(request, user_id):
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 1:
        current_user.user_type = 2
        current_user.save()
    members = User.objects.filter(user_type = 1)
    officers =  User.objects.filter(user_type = 2)
    members_and_officers = members | officers
    return render(request, 'members_and_officers_for_clubowner.html', {'members_and_officers': members_and_officers})

def demote(request, user_id):
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 2:
        current_user.user_type = 1
        current_user.save()
    members = User.objects.filter(user_type = 1)
    officers =  User.objects.filter(user_type = 2)
    members_and_officers = members | officers
    return render(request, 'members_and_officers_for_clubowner.html', {'members_and_officers': members_and_officers})


@login_required
def waiting_list(request):
    current_user = request.user
    if current_user.user_type == 0:
        return render(request, 'waiting_list.html')
    return render(request, 'home.html')


@login_required
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('home')
    else:
        form = UserForm(instance=current_user)
    return render(request, 'profile.html', {'form': form})

@login_required
def password(request):
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
