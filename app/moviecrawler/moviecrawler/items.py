# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviecrawlerItem(scrapy.Item):
    title = scrapy.Field()  # 타이틀
    summary = scrapy.Field()  # 줄거리
    image = scrapy.Field()  # 이미지
    genre = scrapy.Field()  # 장르
    contents_rating = scrapy.Field()  # 관람등급
    directors = scrapy.Field()  # 감독
    actor = scrapy.Field()  # 배우
