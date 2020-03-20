from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    email = models.EmailField('이메일', unique=True)
    password = models.CharField()
    profile = models.ForeignKey(on_delete=models.Model)


class Profile(models.Model):
    name = models.CharField(max_length=150, blank=True)
    image = models.ImageField(blank=True)
