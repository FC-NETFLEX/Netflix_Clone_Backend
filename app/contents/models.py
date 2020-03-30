from django.db import models


class Contents(models.Model):
    contents_title = models.CharField(max_length=150)
    contents_summary = models.TextField(blank=True)
    contents_image = models.ImageField(upload_to='contents/image/', blank=True)
    contents_logo = models.ImageField(upload_to='contents/logo/', blank=True)
    contents_rating = models.CharField(max_length=64)
    contents_length = models.CharField(max_length=64)
    contents_pub_year = models.CharField(max_length=8)
    is_movie = models.BooleanField(default=True)

    actors = models.ManyToManyField('contents.Actor',
                                    related_name='contents',
                                    verbose_name='출연 배우')

    directors = models.ManyToManyField('contents.Director',
                                       related_name='contents',
                                       verbose_name='감독')

    def __str__(self):
        return self.contents_title


class Video(models.Model):
    video_season = models.CharField(max_length=150, blank=True)
    video_title = models.CharField(max_length=150)
    video_summary = models.CharField(max_length=150, blank=True)
    video_url = models.URLField()
    contents = models.ForeignKey('contents.Contents',
                                 on_delete=models.CASCADE,
                                 related_name='videos',
                                 verbose_name='컨텐츠',
                                 null=True)

    def __str__(self):
        return self.video_url


class Category(models.Model):
    category_name = models.CharField(max_length=150)
    contents = models.ManyToManyField('contents.Contents',
                                      related_name='categories',
                                      verbose_name='카테고리')

    def __str__(self):
        return self.category_name


class Actor(models.Model):
    actor_name = models.CharField(max_length=50)

    def __str__(self):
        return self.actor_name


class Director(models.Model):
    director_name = models.CharField(max_length=50)

    def __str__(self):
        return self.director_name
