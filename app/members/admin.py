from django.contrib import admin
# Register your models here.
from django.contrib.auth import get_user_model

from .forms import IconTypeChoiceForm
from .models import Profile, ProfileIcon, Watching

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'profile_name', 'is_kids', 'profile_icon')


@admin.register(ProfileIcon)
class ProfileIconAdmin(admin.ModelAdmin):
    fields = ('icon', 'icon_type')
    form = IconTypeChoiceForm

    list_display = ('icon', 'icon_type')


@admin.register(Watching)
class WatchingAdmin(admin.ModelAdmin):
    pass
