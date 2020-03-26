from bs4 import BeautifulSoup
import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        response = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
        html = response.text





#타이틀
# 이미지
# 줄거리
# 장르
# 등급
# 감독
# 배우
# 개봉연도
# 영상시