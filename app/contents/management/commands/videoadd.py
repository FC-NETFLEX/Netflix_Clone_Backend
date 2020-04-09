import random

import boto3
from django.core.management import BaseCommand

from config.settings.base import SECRETS, MEDIA_URL
from contents.models import Contents, Video


class Command(BaseCommand):
    def handle(self, *args, **options):
        video_url_list = []
        s3 = boto3.client('s3',
                          aws_access_key_id=SECRETS['AWS_ACCESS_KEY_ID'],
                          aws_secret_access_key=SECRETS['AWS_SECRET_ACCESS_KEY'])
        response = s3.list_objects_v2(
            Bucket='fc-netflex',
            Prefix='video/movie/',
            MaxKeys=100)
        video_list = response['Contents'][1:]

        for video in video_list:
            video_url_list.append(MEDIA_URL + video['Key'])

        for contents in Contents.objects.all():
            idx = random.randint(0, len(video_url_list) - 1)
            video = Video.objects.create(video_url=video_url_list[idx])
            contents.videos.add(video)

        return self.stdout.write('video 추가 완료')
