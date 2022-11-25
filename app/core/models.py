"""
Database models
"""
from django.conf import settings
from email.policy import default
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
import calendar
from datetime import date, datetime

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""

        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CitizenStatus(models.TextChoices):
    Permanent = "Permanent resident"
    Temporaire = "Temporary resident"
    Canadien = "Canadian citizen"
    Refugie = "Refugie"

class MaritalStatus(models.TextChoices):
    Single = "Single"
    Married = "Married"
    Divorced = "Divorced"



class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    # Identification of user
    first_name = models.CharField(max_length=255, blank = False,)
    last_name = models.CharField(max_length=255, blank = False,)
    email = models.EmailField(max_length=255, unique=True, blank = False)
    phone = models.CharField(max_length=155, unique=True, blank=False)

    social_number = models.CharField(
        max_length=50,
        unique=True,
        null = True,
        blank = True
    )

    driving_license = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null = True
    )

    citizen_status = models.CharField(
        max_length = 50,
        choices = CitizenStatus.choices,
        default = CitizenStatus.Permanent,
        blank=True,
        null = True
    )
    marital_status = models.CharField(
        max_length = 50,
        choices = MaritalStatus.choices,
        default = MaritalStatus.Single,
        blank=True,
        null = True
    )
    profile_image = models.ImageField(
        upload_to ='uploads/UserImage',
        null = True,
        blank = True,
        default ="noimage"
    )

    # Full Adress of user
    street_number = models.CharField(
        max_length = 10,
        blank=True,
        null = True
    )
    street_name = models.CharField(
        max_length=155,
        blank=True,
        null = True,
        default = "Canada"
    )

    postal_code = models.CharField(
        max_length=155,
        blank=True,
        null = True
    )

    metro_location = models.CharField(
        max_length=155,
        blank = False,
    )
    town = models.CharField(
        max_length=155,
        blank=True,
        null = True,
        default = "Montréal"
    )
    province = models.CharField(
        max_length=155,
        blank=True,
        null = True,
        default = "Québec"
    )
    country = models.CharField(
        max_length=155,
        blank=True,
        null = True,
        default = "Canada"
    )

    accept_tnc = models.BooleanField(default=True)

    # Status of user
    is_worker = models.BooleanField(default=False)
    is_job_owner = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(verbose_name = "last login", blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return str(self.id) + "--" + self.email
