"""Static views of the clubs app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'dashboard.html')
