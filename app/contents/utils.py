import random
from collections import Counter

from django.db.models import Max, Min

from contents.models import Contents


def get_ad_contents():
    max_id = Contents.objects.filter(preview_video__isnull=False).aggregate(max_id=Max("id"))['max_id']
    min_id = Contents.objects.filter(preview_video__isnull=False).aggregate(min_id=Min("id"))['min_id']
    while True:
        pk = random.randint(min_id, max_id)
        contents = Contents.objects.filter(pk=pk).first()
        if contents:
            return contents


def get_top_contents():
    max_id = Contents.objects.filter(contents_pub_year='2020').aggregate(max_id=Max("id"))['max_id']
    min_id = Contents.objects.filter(contents_pub_year='2020').aggregate(min_id=Min("id"))['min_id']
    while True:
        pk = random.randint(min_id, max_id)
        contents = Contents.objects.filter(pk=pk).first()
        if contents:
            return contents


def get_preview_video():
    max_id = Contents.objects.filter(preview_video__isnull=False).aggregate(max_id=Max("id"))['max_id']
    min_id = Contents.objects.filter(preview_video__isnull=False).aggregate(min_id=Min("id"))['min_id']
    video_list = []
    while True:
        if len(video_list) == 10:
            break
        else:
            pk = random.randint(min_id, max_id)
            video_list.append(pk)
    return video_list


def get_top10_contents():
    top10_list = []
    like_contents = Contents.objects.filter(like_profiles__isnull=False)
    select_contents = Contents.objects.filter(select_profiles__isnull=False)
    counter = (Counter(like_contents) + Counter(select_contents)).most_common(10)

    for contents, _ in counter:
        top10_list.append(contents)

    return top10_list
