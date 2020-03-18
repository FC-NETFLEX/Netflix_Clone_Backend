from django.db import models


class Content(models.Model):
    summary = models.CharField(max_length=150, blank=True)
    thumbnail = models.ImageField(blank=True)
    title = models.CharField(max_length=150, blank=True)


class Video(models.Model):
    season = models.CharField(max_length=150, blank=True)
    episode = models.CharField(max_length=150, blank=True)
    summary = models.CharField(max_length=150, blank=True)
    url = models.URLField(max_length=200)


class Actor(models.Model):
    name = models.CharField(max_length=150, blank=True)


class Director(models.Model):
    name = models.CharField(max_length=150, blank=True)
