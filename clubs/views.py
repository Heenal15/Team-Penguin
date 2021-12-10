from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import RegisterForm, LogInForm, UserForm, PasswordForm, ClubForm
from .models import User, Club
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

def log_in(request):
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
                messages.add_message(request, messages.ERROR, "Username And Password Do Not Match")
        else:
            messages.add_message(request, messages.ERROR, "You Have Provided An Invalid Input")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

@login_required
def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required
def home(request):
    return render(request, 'home.html')
  
def register(request):
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

#used to check if current user has privaleges to view page
def is_member(user):
    return (user.is_authenticated and user.user_type == 1)

def is_club_officer(user):
    return (user.is_authenticated and user.user_type == 2)

def is_club_owner(user):
    return (user.is_authenticated and user.user_type == 3)

def is_club_owner_or_officer(user):
    return (user.is_authenticated and user.user_type == 2 or user.user_type == 3)

def is_club_owner_or_officer_or_member(user):
    return (user.is_authenticated and user.user_type == 1 or user.user_type == 2 or user.user_type == 3)

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

@user_passes_test(is_club_owner_or_officer, login_url='unauthorised_access', redirect_field_name=None)
def applicant_list(request):
    applicants = User.objects.filter(user_type = 0)
    return render(request, 'applicant_list.html', {'applicants': applicants})

def memberlist_Clubowner(request):
    users = User.objects.all()
    return render(request, 'memberlist_Clubowner.html', {'users': users})

@user_passes_test(is_club_owner_or_officer, login_url='unauthorised_access', redirect_field_name=None)
def show_user(request, user_id):
    try:
        user = User.objects.get(id = user_id)
    except ObjectDoesNotExist:

        #return redirect('full_user_list','memberlist_Clubowner')

        return redirect('home')

    else:
        return render(request, 'show_user.html', {'user': user})

@user_passes_test(is_club_owner_or_officer_or_member, login_url='unauthorised_access', redirect_field_name=None)
def show_member(request, user_id):
    try:
        user = User.objects.get(id = user_id)
    except ObjectDoesNotExist:
        return redirect('member_list')
    else:
        return render(request, 'show_member.html', {'user': user})

@login_required
def approve(request, user_id):
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 0:
        current_user.user_type = 1
        current_user.save()
    applicants = User.objects.filter(user_type = 0)
    return render(request, 'applicant_list.html', {'applicants': applicants})

@login_required
def unapprove(request, user_id):
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 0:
        current_user.delete()
    applicants = User.objects.filter(user_type = 0)
    return render(request, 'applicant_list.html', {'applicants': applicants})

@login_required
def promote(request, user_id):
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 1:
        current_user.user_type = 2
        current_user.save()
    members = User.objects.filter(user_type = 1)
    officers =  User.objects.filter(user_type = 2)
    members_and_officers = members | officers
    return render(request, 'members_and_officers_for_clubowner.html', {'members_and_officers': members_and_officers})

@login_required
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
def officers(request):
    officers = User.objects.filter(user_type = 2)
    return render(request, 'officers.html', {'officers': officers})

def load_club(request):
    return render(request, 'load_club.html',)

@login_required
def make_owner(request, user_id):
    user = request.user
    current_user = User.objects.get(id = user_id)
    # Current club owner becomes an officer
    user.user_type = 2
    user.save()
    if User.objects.filter(user_type = 3).exists():
        officers = User.objects.filter(user_type = 2)
    else:
        current_user.user_type = 3
        current_user.save()
        officers = User.objects.filter(user_type = 2)
    return render(request, 'officers.html', {'officers': officers})


def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'club_list.html', {'clubs': clubs})

@login_required
def profile(request):
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

@login_required
def create_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            club = Club.objects.create(
                club_name=form.cleaned_data.get('club_name'),
                club_location=form.cleaned_data.get('club_location'),
                club_description=form.cleaned_data.get('club_description')
            )
    else:
        form = ClubForm()
    return render(request, 'create_club.html', {'form': form})
