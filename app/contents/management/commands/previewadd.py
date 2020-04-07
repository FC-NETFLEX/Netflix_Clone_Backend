import random

import boto3
from django.core.management import BaseCommand

from config.settings.base import SECRETS
from contents.models import Contents


class Command(BaseCommand):
    def handle(self, *args, **options):
        preview_video_list = []
        s3 = boto3.client('s3',
                          aws_access_key_id=SECRETS['AWS_ACCESS_KEY_ID'],
                          aws_secret_access_key=SECRETS['AWS_SECRET_ACCESS_KEY'])
        response = s3.list_objects_v2(
            Bucket='fc-netflex',
            Prefix='video/preview',
            MaxKeys=100)
        response['Contents'].pop(0)
        for item in response['Contents']:
            preview_video_list.append("https://fc-netflex.s3.ap-northeast-2.amazonaws.com/" + item['Key'])

        contents_list = Contents.objects.order_by('pk')[:100]

        for contents in contents_list:
            idx = random.randint(0, len(preview_video_list) - 1)
            contents.preview_video = preview_video_list[idx]
            contents.save()
        return self.stdout.write('preview video 추가 완료')
