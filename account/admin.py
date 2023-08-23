from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.models import User

# from .forms import UserAdminCreationForm, UserAdminChangeForm
admin.site.register(User)
