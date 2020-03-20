from django.db import models


class Content(models.Model):
    title = models.CharField(max_length=150)
    summary = models.CharField(max_length=150, blank=True)
    thumbnail = models.ImageField(blank=True)
    is_movie = models.BooleanField(default=False)


class Video(models.Model):
    season = models.CharField(max_length=150, blank=True)
    episode = models.CharField(max_length=150)
    summary = models.CharField(max_length=150, blank=True)
    url = models.URLField(max_length=200)
    content = models.ForeignKey('contents.Content',
                                on_delete=models.CASCADE,
                                related_name='video',
                                verbose_name='컨텐츠',
                                null=True)


class SubCategory(models.Model):
    name = models.CharField(max_length=150)
    content = models.ForeignKey('contents.Content',
                                on_delete=models.CASCADE,
                                related_name='subcategories',
                                verbose_name='카테고리',
                                null=True)
