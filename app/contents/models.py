from django.db import models


class Contents(models.Model):
    CONTENTS_RATING = (
        (0, '전체이용가'),
        (12, '12세이용가'),
        (15, '15세이용가'),
        (18, '청소년이용불가'),
    )
    contents_title = models.CharField(max_length=150)
    contents_summary = models.TextField(blank=True)
    contents_image = models.ImageField(blank=True)
    contents_logo = models.ImageField(blank=True)
    contents_rating = models.IntegerField(choices=CONTENTS_RATING, default=0)
    contents_length = models.CharField(max_length=64, blank=True)
    contents_pub_year = models.CharField(max_length=8, blank=True)
    is_movie = models.BooleanField(default=True)

    actors = models.ManyToManyField('contents.Actor',
                                    related_name='contents',
                                    verbose_name='출연 배우')

    directors = models.ManyToManyField('contents.Director',
                                       related_name='contents',
                                       verbose_name='감독')


class Video(models.Model):
    video_season = models.CharField(max_length=150, blank=True)
    video_title = models.CharField(max_length=150)
    video_summary = models.CharField(max_length=150, blank=True)
    video_url = models.URLField(max_length=200)
    contents = models.ForeignKey('contents.Contents',
                                 on_delete=models.CASCADE,
                                 related_name='videos',
                                 verbose_name='컨텐츠',
                                 null=True)


class Category(models.Model):
    category_name = models.CharField(max_length=150)
    contents = models.ForeignKey('contents.Contents',
                                 on_delete=models.CASCADE,
                                 related_name='categories',
                                 verbose_name='카테고리',
                                 null=True)


class Actor(models.Model):
    actor_name = models.CharField(max_length=50)


class Director(models.Model):
    director_name = models.CharField(max_length=50)
