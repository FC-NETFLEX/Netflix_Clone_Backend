import random
from collections import Counter

from contents.models import Contents


def get_ad_contents(queryset):
    """
    Contents의 queryset을 받아서 preview video가 존재하는 contents를 랜덤으로 1개 리턴
    :param queryset: Contents queryset
    :return: contents object
    """
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
    """
    Contents의 queryset을 받아서 2010년 이후 출시된 영화 중 로고가 있는 영화를 랜덤으로 1개 리턴
    :param queryset: Contents queryset
    :return: contents object
    """
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
    """
    Contents의 queryset을 받아서 preview_video가 있고 로고가 있는 contents를 랜덤으로 10개 리턴
    :param queryset: Contents queryset
    :return: Contents queryset
    """
    contents_list = queryset.filter(preview_video__isnull=False, contents_logo__isnull=False)
    contents_list = contents_list.order_by('?')[:10]
    return contents_list


def get_popular_contents(queryset, count):
    """
    like와 select 수가 많은 contents를 count 수 만큼 리턴
    :param queryset: Contents queryset
    :param count: count
    :return: Contents queryset
    """
    like_contents = queryset.filter(like_profiles__isnull=False)
    select_contents = queryset.filter(select_profiles__isnull=False)
    counter = (Counter(like_contents) + Counter(select_contents)).most_common(count)
    pk_list = [contents.pk for contents, _ in counter]
    top10_contents_queryset = Contents.objects.filter(pk__in=pk_list)
    return top10_contents_queryset
