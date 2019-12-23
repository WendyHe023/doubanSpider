# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy

from xingren.models.es_types import DoubanType


class DoubanItem(scrapy.Item):
    title = scrapy.Field()
    original_title = scrapy.Field()

    douban_link = scrapy.Field()
    year = scrapy.Field()
    lang = scrapy.Field()
    country = scrapy.Field()
    runtime = scrapy.Field()
    release_at = scrapy.Field()
    overview = scrapy.Field()
    genres = scrapy.Field()
    rating = scrapy.Field()
    imdb = scrapy.Field()

    season_count = scrapy.Field()

    small_image = scrapy.Field()
    # big_image = scrapy.Field()

    directors = scrapy.Field()
    writers = scrapy.Field()
    casts = scrapy.Field()

    def save_to_es(self):
        douban = DoubanType()
        douban.title = self['title']
        douban.douban_link = self['douban_link']
        douban.year = self['year']
        douban.lang = self['lang']
        douban.country = self['country']
        douban.runtime = self['runtime']
        douban.release_at = self['release_at']
        douban.overview = self['overview']
        douban.genres = self['genres']
        douban.rating = self['rating']
        douban.imdb = self['imdb']

        douban.original_title = self['original_title']
        douban.season_count = self['season_count']

        douban.small_image = self['small_image']
        # douban.big_image = self['big_image']

        douban.directors = self['directors']
        douban.writers = self['writers']
        douban.casts = self['casts']

        douban.save()

        return douban
