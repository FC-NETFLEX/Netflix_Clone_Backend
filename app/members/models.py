from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        user = User.objects.create(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = User.objects.create_user(email=email, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('이메일', max_length=128, unique=True)
    password = models.CharField('비밀번호', max_length=128)
    created = models.DateTimeField('생성일자', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return f'{self.email}'

    @property
    def is_staff(self):
        return self.is_superuser


class Profile(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='프로필',
                             related_name='profile',
                             null=True
                             )
    name = models.CharField('이름', max_length=150)
    image = models.ImageField('프로필이미지', blank=True)
    is_kids = models.BooleanField('키즈', default=False)
    created = models.DateTimeField('생성일자', default=timezone.now)
    watching_videos = models.ManyToManyField('contents.Video',
                                             verbose_name='재생 중인 비디오',
                                             related_name='profiles')

    def __str__(self):
        return f'{self.user.email} : {self.name}'
