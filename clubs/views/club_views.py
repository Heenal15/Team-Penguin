""" The views of the club """
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from clubs.forms import ClubForm
from clubs.models import Club
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def load_club(request):
    """ Load all the avaible clubs """
    return render(request, 'load_club.html',)

def club_list(request):
    """ Display a list of all clubs """
    clubs = Club.objects.all()
    return render(request, 'club_list.html', {'clubs': clubs})

@login_required
def club_sign_up(request):
    """ Able to fill in a club sign up form to create a club """
    form = ClubForm(data=request.POST)
    return render(request, 'club_sign_up.html', {'form': form})

@login_required
def create_club(request):
    """ Ability to create a club """
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