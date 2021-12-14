from django.shortcuts import redirect, render
from clubs.forms import ClubForm
from clubs.models import User, Club
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist

#used to check if current user has privileges to view page if the pages are requested by typing directly into URL
def is_member(user):
    if (user.is_authenticated):
        return user.user_type == 1
    else:
        return False

def is_club_officer(user):
    if (user.is_authenticated):
        return user.user_type == 2
    else:
        return False

def is_club_owner(user):
    if (user.is_authenticated):
        return user.user_type == 3
    else:
        return False

def is_club_owner_or_officer(user):
    if (user.is_authenticated):
        return (user.user_type == 2 or user.user_type == 3)
    else:
        return False

def is_club_owner_or_officer_or_member(user):
    if (user.is_authenticated):
        return (user.user_type == 1 or user.user_type == 2 or user.user_type == 3)
    else:
        return False

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

@user_passes_test(is_club_owner_or_officer, login_url='unauthorised_access', redirect_field_name=None)
def approve(request, user_id):
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 0:
        current_user.user_type = 1
        current_user.save()
    applicants = User.objects.filter(user_type = 0)
    return render(request, 'applicant_list.html', {'applicants': applicants})

@user_passes_test(is_club_owner_or_officer, login_url='unauthorised_access', redirect_field_name=None)
def unapprove(request, user_id):
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 0:
        current_user.delete()
    applicants = User.objects.filter(user_type = 0)
    return render(request, 'applicant_list.html', {'applicants': applicants})

@user_passes_test(is_club_owner, login_url='unauthorised_access', redirect_field_name=None)
def promote(request, user_id):
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 1:
        current_user.user_type = 2
        current_user.save()
    members = User.objects.filter(user_type = 1)
    officers =  User.objects.filter(user_type = 2)
    members_and_officers = members | officers
    return render(request, 'members_and_officers_for_clubowner.html', {'members_and_officers': members_and_officers})

@user_passes_test(is_club_owner, login_url='unauthorised_access', redirect_field_name=None)
def demote(request, user_id):
    current_user = User.objects.get(id = user_id)
    if current_user.user_type == 2:
        current_user.user_type = 1
        current_user.save()
    members = User.objects.filter(user_type = 1)
    officers =  User.objects.filter(user_type = 2)
    members_and_officers = members | officers
    return render(request, 'members_and_officers_for_clubowner.html', {'members_and_officers': members_and_officers})

@user_passes_test(is_club_owner, login_url='unauthorised_access', redirect_field_name=None)
def officers(request):
    officers = User.objects.filter(user_type = 2)
    return render(request, 'officers.html', {'officers': officers})

def load_club(request):
    return render(request, 'load_club.html',)

@user_passes_test(is_club_owner, login_url='unauthorised_access', redirect_field_name=None)
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
def club_sign_up(request):
    form = ClubForm(data=request.POST)
    return render(request, 'club_sign_up.html', {'form': form})

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
