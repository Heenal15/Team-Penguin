"""Forms for the clubs app."""
from django import forms
from .models import User, Club
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
        return user

class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'experience', 'statement']
        widgets = { 'bio': forms.Textarea(), 'statement':forms.Textarea()}

class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='New Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Previous password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""

        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(email=self.user.email, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user

class RegisterForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'experience', 'statement']
        widgets = {'bio':forms.Textarea(), 'statement':forms.Textarea()}

    def save(self):
        """Create a new user."""

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

class ClubForm(forms.ModelForm):
    """Form for creation of a club"""

    class Meta:
        model = Club
        fields = ['club_name', 'club_location', 'club_description']
        widgets = {'club_location': forms.Textarea(), 'club_description': forms.Textarea()}
