from django.db import models


class Contents(models.Model):
    contents_title = models.CharField(max_length=150)
    contents_title_english = models.CharField(max_length=150, blank=True)
    contents_summary = models.TextField(blank=True)
    contents_image = models.ImageField(upload_to='contents/image/', blank=True)
    contents_logo = models.ImageField(upload_to='contents/logo/', null=True)
    contents_rating = models.CharField(max_length=64)
    contents_length = models.CharField(max_length=64)
    contents_pub_year = models.CharField(max_length=8)
    is_movie = models.BooleanField(default=True)
    preview_video = models.URLField(null=True)

    actors = models.ManyToManyField('contents.Actor',
                                    related_name='contents',
                                    verbose_name='출연 배우')

    directors = models.ManyToManyField('contents.Director',
                                       related_name='contents',
                                       verbose_name='감독')

    class Meta:
        verbose_name = 'contents'
        verbose_name_plural = 'contents'

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
    CATEGORY_CHOICE = (
        ('1', '드라마'),
        ('2', '판타지'),
        ('3', '서부'),
        ('4', '공포'),
        ('5', '로맨스'),
        ('6', '모험'),
        ('7', '스릴러'),
        ('8', '느와르'),
        ('9', '컬트'),
        ('10', '다큐멘터리'),
        ('11', '코미디'),
        ('12', '가족'),
        ('13', '미스터리'),
        ('14', '전쟁'),
        ('15', '애니메이션'),
        ('16', '범죄'),
        ('17', '뮤지컬'),
        ('18', 'SF'),
        ('19', '액션'),
        ('20', '무협'),
        ('21', '에로'),
        ('22', '서스펜스'),
        ('23', '서사'),
        ('24', '블랙코미디'),
        ('25', '실험'),
        ('26', '영화카툰'),
        ('27', '영화음악'),
        ('28', '영화패러디포스터')
    )
    category_name = models.CharField(max_length=150, choices=CATEGORY_CHOICE)
    contents = models.ManyToManyField('contents.Contents',
                                      related_name='categories',
                                      verbose_name='카테고리')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.get_category_name_display()


class Actor(models.Model):
    actor_name = models.CharField(max_length=50)

    def __str__(self):
        return self.actor_name


class Director(models.Model):
    director_name = models.CharField(max_length=50)

    def __str__(self):
        return self.director_name
