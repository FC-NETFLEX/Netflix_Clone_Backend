import random

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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
    email = models.EmailField(_('이메일'), max_length=128, unique=True)
    password = models.CharField(_('비밀번호'), max_length=128)
    created = models.DateTimeField(_('생성일자'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return self.email


class ProfileIcon(models.Model):
    icon_name = models.CharField(_('아이콘 이름'), max_length=128)
    icon = models.ImageField(_('아이콘'), upload_to='profile/icon/')
    icon_category = models.ForeignKey('members.ProfileIconCategory',
                                      verbose_name=_('아이콘 카테고리'),
                                      related_name='profileIcons',
                                      on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('icon')
        verbose_name_plural = _('icons')

    def __str__(self):
        return self.icon_name


class ProfileIconCategory(models.Model):
    category_name = models.CharField(_('아이콘 카테고리'), max_length=128)

    class Meta:
        verbose_name = _('icon category')
        verbose_name_plural = _('icon categories')

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
                             verbose_name=_('프로필'),
                             related_name='profiles',
                             on_delete=models.CASCADE,
                             )

    profile_name = models.CharField(_('이름'), max_length=150)
    is_kids = models.BooleanField(_('키즈'), default=False)
    created = models.DateTimeField(_('생성일자'), default=timezone.now)
    watching_videos = models.ManyToManyField('contents.Video',
                                             through='members.Watching',
                                             verbose_name=_('시청 중인 비디오'),
                                             related_name='profiles',
                                             )

    select_contents = models.ManyToManyField('contents.Contents',
                                             verbose_name=_('찜한 컨텐츠'),
                                             related_name='select_profiles',
                                             )

    like_contents = models.ManyToManyField('contents.Contents',
                                           verbose_name=_('좋아요'),
                                           related_name='like_profiles',
                                           )

    profile_icon = models.ForeignKey('members.ProfileIcon',
                                     verbose_name=_('프로필 아이콘'),
                                     related_name='profiles',
                                     on_delete=models.SET(get_default_icon))

    def __str__(self):
        return f'{self.user.email} : {self.profile_name}'


class Watching(models.Model):
    video = models.ForeignKey('contents.Video',
                              on_delete=models.CASCADE,
                              verbose_name=_('비디오'),
                              related_name='watching')
    profile = models.ForeignKey('members.Profile',
                                on_delete=models.CASCADE,
                                verbose_name=_('프로필'),
                                related_name='watching')
    playtime = models.PositiveIntegerField(_('재생시간'))
    video_length = models.PositiveIntegerField(_('비디오 길이'))

    class Meta:
        verbose_name = _('watching')
        verbose_name_plural = _('watching')
        constraints = [
            models.UniqueConstraint(fields=['video', 'profile'], name='profile-video')
        ]

    def __str__(self):
        return f'{self.video.pk}, {self.profile.profile_name}'
