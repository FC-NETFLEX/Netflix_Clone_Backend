from django.contrib import admin
# Register your models here.
from django.contrib.auth import get_user_model

from members.models import Profile

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
