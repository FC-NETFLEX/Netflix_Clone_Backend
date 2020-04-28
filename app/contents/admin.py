from django.contrib import admin

from contents.models import Contents, Video, Category


# Register your models here.


class Videoinline(admin.TabularInline):
    model = Video
    fields = [
        'video_url',
    ]
    extra = 0


@admin.register(Contents)
class ContentsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'contents_title', 'contents_rating', 'preview_video']
    ordering = ['pk']
    search_fields = ['contents_title']
    inlines = [
        Videoinline,
    ]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['pk']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
