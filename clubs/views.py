from django.shortcuts import render


def log_in(request):
    return render(request, 'log_in.html')

def home(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')
