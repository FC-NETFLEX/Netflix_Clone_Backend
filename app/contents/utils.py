import random
from collections import Counter

from contents.models import Contents


def get_ad_contents(queryset):
    contents_list = queryset.filter(preview_video__isnull=False)
    max_int = contents_list.count() - 1
    if max_int < 0:
        return
    while True:
        idx = random.randint(0, max_int)
        contents = contents_list[idx]
        if contents:
            return contents


def get_top_contents(queryset):
    contents_list = queryset.filter(contents_pub_year__gte='2010', contents_logo__isnull=False)
    max_int = contents_list.count() - 1
    if max_int < 0:
        return
    while True:
        idx = random.randint(0, max_int)
        contents = contents_list[idx]
        if contents:
            return contents


def get_preview_video(queryset):
    contents_list = queryset.filter(preview_video__isnull=False)
    max_int = contents_list.count() - 1
    if max_int < 0:
        return
    video_list = []
    pk_list = []
    while True:
        if len(video_list) == max_int or len(video_list) == 10:
            break
        pk = random.randint(0, max_int)
        if pk in pk_list:
            continue
        pk_list.append(pk)
        video_list.append(contents_list[pk])
    return video_list


def get_popular_contents(queryset, count):
    top10_list = []
    like_contents = queryset.filter(like_profiles__isnull=False)
    select_contents = queryset.filter(select_profiles__isnull=False)
    counter = (Counter(like_contents) + Counter(select_contents)).most_common(count)
    for contents, _ in counter:
        top10_list.append(contents)
    pk_list = [contents.pk for contents in top10_list]
    top10_contents_queryset = Contents.objects.filter(pk__in=pk_list)
    return top10_contents_queryset
