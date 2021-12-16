""" File to display the correct render of a a logged in user """
from django.shortcuts import redirect, render

def homepage(request):
    """ Render homepage for all visitors to the site """
    return render(request, 'homepage.html')
