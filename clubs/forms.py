from django import forms
from .models import User
from django.core.validators import RegexValidator


class LogInForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'experience', 'statement', 'user_type']
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
    user_type = forms.IntegerField(label='User Type')

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'confirmation doesnt match password')

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
            email=self.cleaned_data.get('email'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            bio=self.cleaned_data.get('bio'),
            experience=self.cleaned_data.get('experience'),
            statement=self.cleaned_data.get('statement'),
            password=self.cleaned_data.get('new_password')
        )
        return user

class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'experience', 'statement']
        widgets = { 'bio': forms.Textarea(), 'experience':forms.Textarea(), 'statement':forms.Textarea()}

class PasswordForm(forms.Form):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())
    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')
