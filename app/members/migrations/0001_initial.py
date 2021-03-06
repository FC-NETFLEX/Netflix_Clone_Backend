
# Generated by Django 2.2.11 on 2020-04-01 12:04


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('contents', '0001_initial'),

    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=128, unique=True, verbose_name='이메일')),
                ('password', models.CharField(max_length=128, verbose_name='비밀번호')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='생성일자')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_name', models.CharField(max_length=150, verbose_name='이름')),
                ('is_kids', models.BooleanField(default=False, verbose_name='키즈')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='생성일자')),
                ('like_contents', models.ManyToManyField(related_name='like_profiles', to='contents.Contents', verbose_name='평가한 컨텐츠')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon_name', models.CharField(max_length=128, verbose_name='아이콘 이름')),
                ('icon', models.ImageField(upload_to='profile/icon/', verbose_name='아이콘')),
                ('icon_category', models.CharField(max_length=64, verbose_name='아이콘 타입')),
            ],
        ),
        migrations.CreateModel(
            name='Watching',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playtime', models.PositiveIntegerField(verbose_name='재생시간')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watching', to='members.Profile', verbose_name='프로필')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watching', to='contents.Video', verbose_name='비디오')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_icon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='members.ProfileIcon', verbose_name='프로필 이미지'),
        ),
        migrations.AddField(
            model_name='profile',
            name='select_contents',
            field=models.ManyToManyField(related_name='select_profiles', to='contents.Contents', verbose_name='찜한 컨텐츠'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to=settings.AUTH_USER_MODEL, verbose_name='프로필'),
        ),
        migrations.AddField(
            model_name='profile',
            name='watching_videos',
            field=models.ManyToManyField(related_name='profiles', through='members.Watching', to='contents.Video', verbose_name='재생 중인 비디오'),
        ),
    ]
