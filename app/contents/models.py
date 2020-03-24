from django.db import models


class Contents(models.Model):
    CONTENTS_RATING = (
        (0, '전체이용가'),
        (12, '12세이용가'),
        (15, '15세이용가'),
        (18, '청소년이용불가'),
    )
    # contents 제목
    contents_title = models.CharField(max_length=150)
    # contents 줄거리
    contents_summary = models.TextField(blank=True)
    # contents 메인 이미지
    contents_image = models.ImageField(blank=True)
    # contents 등급
    contents_rating = models.IntegerField(choices=CONTENTS_RATING, default=0)
    # contents 타입
    is_movie = models.BooleanField(default=True)


class Video(models.Model):
    # 시즌 정보    ex)시즌 1, 시즌 2
    video_season = models.CharField(max_length=150, blank=True)
    # 제목        ex) 1화, 2화  -> 꼭 이런 제목이 아닐 수도 있다.
    video_title = models.CharField(max_length=150)
    # 줄거리
    video_summary = models.CharField(max_length=150, blank=True)
    # 영상 주소
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
