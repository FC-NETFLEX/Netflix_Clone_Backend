import random

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


class ProfileIcon(models.Model):
    icon_name = models.CharField('아이콘 이름', max_length=128)
    icon = models.ImageField('아이콘', upload_to='profile/icon/')
    icon_category = models.ForeignKey('members.ProfileIconCategory',
                                      verbose_name='아이콘 카테고리',
                                      related_name='profileIcons',
                                      on_delete=models.CASCADE)

    def __str__(self):
        return self.icon.url


class ProfileIconCategory(models.Model):
    category_name = models.CharField('아이콘 카테고리', max_length=128)

    def __str__(self):
        return self.category_name


def get_default_icon():
    """
        대표 아이콘 중 하나를 랜덤으로 선택해서 return
    """
    category = ProfileIconCategory.objects.get(category_name='대표 아이콘')
    return category.profileIcons.all()[random.randint(0, category.profileIcons.count())]


class Profile(models.Model):
    user = models.ForeignKey('members.User',
                             verbose_name='프로필',
                             related_name='profiles',
                             on_delete=models.CASCADE,
                             )

    profile_name = models.CharField('이름', max_length=150)
    is_kids = models.BooleanField('키즈', default=False)
    created = models.DateTimeField('생성일자', default=timezone.now)
    watching_videos = models.ManyToManyField('contents.Video',
                                             through='members.Watching',
                                             verbose_name='재생 중인 비디오',
                                             related_name='profiles',
                                             )

    select_contents = models.ManyToManyField('contents.Contents',
                                             verbose_name='찜한 컨텐츠',
                                             related_name='select_profiles',
                                             )

    like_contents = models.ManyToManyField('contents.Contents',
                                           verbose_name='평가한 컨텐츠',
                                           related_name='like_profiles',
                                           )

    profile_icon = models.ForeignKey('members.ProfileIcon',
                                     verbose_name='프로필 이미지',
                                     related_name='profiles',
                                     on_delete=models.SET(get_default_icon))

    def __str__(self):
        return f'{self.user.email} : {self.profile_name}'


class Watching(models.Model):
    video = models.ForeignKey('contents.Video',
                              on_delete=models.CASCADE,
                              verbose_name='비디오',
                              related_name='watching')
    profile = models.ForeignKey('members.Profile',
                                on_delete=models.CASCADE,
                                verbose_name='프로필',
                                related_name='watching')
    playtime = models.PositiveIntegerField('재생시간')
    video_length = models.PositiveIntegerField('비디오 길이')

    class Meta:
        unique_together = ('video', 'profile')
