from django.contrib import admin
# Register your models here.
from django.contrib.auth import get_user_model

from .models import Profile, ProfileIcon, Watching, ProfileIconCategory

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'profile_name', 'is_kids', 'profile_icon')


class ProfileIconInline(admin.TabularInline):
    model = ProfileIcon
    fields = ('icon_name', 'icon')


@admin.register(ProfileIcon)
class ProfileIconAdmin(admin.ModelAdmin):
    fields = ('icon', 'icon_name', 'icon_category')
    list_display = ('icon', 'icon_name', 'icon_category')


@admin.register(ProfileIconCategory)
class ProfileIconCategoryAdmin(admin.ModelAdmin):
    inlines = [
        ProfileIconInline,
    ]


@admin.register(Watching)
class WatchingAdmin(admin.ModelAdmin):
    pass
