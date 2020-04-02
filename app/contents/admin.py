from django.contrib import admin

from contents.models import Contents, Video, Category


# Register your models here.


@admin.register(Contents)
class ContentsAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
