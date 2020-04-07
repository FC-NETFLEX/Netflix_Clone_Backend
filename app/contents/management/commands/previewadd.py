import boto3
import random
from django.core.management import BaseCommand

from config.settings.base import SECRETS


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

        print(preview_video_list)