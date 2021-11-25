from django.shortcuts import render


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
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
    return render(request, 'register.html')
