"""Models in the clubs app."""

from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from libgravatar import Gravatar

"""Overriding model manager user model with email as username"""
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            **extra_fields
        )
        user.set_password(password)
        user.is_superuser = False
        user.is_staff = False
        user.user_type=0
        user.save(using=self._db) #giving error in tests
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=None, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    """User model used for authentication and club authoring."""

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    USER_TYPE_CHOICES = (
        (0, 'Applicant'),
        (1, 'Member'),
        (2, 'Club Officer'),
        (3, 'Club Owner'),
    )

    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=0)

    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    bio = models.CharField(max_length=520, blank=True)
    experience = models.CharField(max_length=300, blank=True)
    statement = models.CharField(max_length=1000, blank=True)

    #is_waiting_list = True

    objects = UserManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)
