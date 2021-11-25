from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import ApplicationForm, LogInForm
from .models import User
from django.http import HttpResponseForbidden

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
        # Add error message here
        messages.add_message(request, messages.ERROR, "The credentials provided are invalid.")

    form = LogInForm()
    return render(request, 'log_in.html', {'form' : form})

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

def full_user_list(request):
    users = User.objects.all()
    return render(request, 'full_user_list.html', {'users': users})

def member_list(request):
    users = User.objects.all()
    return render(request, 'member_list.html', {'users': users})

def show_user(request, user_id):
    try:
        user = User.objects.get(id = user_id)
    except ObjectDoesNotExist:
        return redirect('full_user_list')
    else:
        return render(request, 'show_user.html', {'user': user})

def show_member(request, user_id):
    try:
        user = User.objects.get(id = user_id)
    except ObjectDoesNotExist:
        return redirect('member_list')
    else:
        return render(request, 'show_member.html', {'user': user})
