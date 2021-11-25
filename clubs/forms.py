from django import forms
from .models import User
from django.core.validators import RegexValidator


class LogInForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'experience', 'statement']
        widgets = {'bio':forms.Textarea(), 'experience':forms.Textarea(), 'statement':forms.Textarea()}
    new_password = forms.CharField(label='Password', widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex = r'[A-Z]',
                message='password must have an uppercase letter'
                ),
            RegexValidator(
                regex = r'[a-z]',
                message='password must have a lowercase letter'
                ),
            RegexValidator(
                regex = r'[0-9]',
                message='password must contain a number'
                ),
            ]
        )
    password_confirmation = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'confirmation doesnt match password')

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            bio=self.cleaned_data.get('bio'),
            experience=self.cleaned_data.get('experience'),
            statement=self.cleaned_data.get('statement'),
            password=self.cleaned_data.get('new_password')
        )
        return user
