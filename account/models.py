from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    UserManager, AbstractBaseUser, PermissionsMixin
)


class CustomUserManager(UserManager):
    def _create_user(self, phone=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone and password.
        """
        user = self.model(phone=phone, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is True and extra_fields.get('is_superuser') is True:
            raise ValueError(
                'Staff user must have is_staff=True and is_superuser=False.')

        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(phone, password, **extra_fields)

# User Model


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # a superuser

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    # Custom fields
    f_name = models.CharField(max_length=20, blank=True, default='')
    l_name = models.CharField(max_length=35, blank=True, default='')
    phone = models.CharField(max_length=11, unique=True, blank=True, default=0)
    profile_pic = models.ImageField(upload_to='static/account/profile',blank=True)
    # True for Dealer || False for Individual
    acc_type = models.BooleanField(default=False)
    ad_limit = models.IntegerField(default=1)
    address = models.CharField(default="N/A", max_length=255)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []  # Add other required fields

    def get_full_name(self):
        return f'{self.f_name} {self.l_name}'

    def get_short_name(self):
        return self.f_name

    # def __str__(self):

    # def has_perm(self, perm, obj=None):
    #     return True  # All users have all permissions

    # def has_module_perms(self, app_label):
    #     return True  # All users have all permissions
