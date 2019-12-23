# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy import Request

from xingren.items import DoubanItem


def get_num(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        num = int(match_re.group(1))
    else:
        num = 0
    return num


def get_date(value):
    match_re = re.match("(\d+)((-\d+)|.*?)((-\d+)|.*?)", value)
    if match_re:
        num = match_re.group(1)
        if match_re.group(3):
            num = num + match_re.group(3)
        else:
            num += "-01"
        if match_re.group(5):
            num = num + match_re.group(5)
        else:
            num += "-01"
    else:
        return 0
    return num


class DoubanquerySpider(scrapy.Spider):
    name = 'doubanQuery'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/tag/#/']

    tags = '电影'
    start = 0
    url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags={tags}&start={start}"

    def start_requests(self):
        for index in range(6000, 6500, 20):
            yield Request(self.url.format(tags=self.tags, start=index), callback=self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        # print(result)
        for data in result['data']:
            img_url = data['cover']
            subject_url = data['url']
            yield Request(url=subject_url, meta={"front_image_url": img_url},
                          callback=self.parse_detail)

    @staticmethod
    def parse_detail(response):
        subject_item = DoubanItem()

        title = response.css("h1>span:nth-child(1)::text").extract_first()
        year = response.css("h1 > span:nth-child(2)::text").extract_first()
        rating = response.css('.rating_num::text').extract_first()
        genres = response.css('#info > span[property$=genre]::text').extract()
        runtime = response.css('#info > span[property$=time]::text').extract_first()
        release_at = response.css('#info > span[property$=Date]::text').extract_first()
        overview = response.css('#link-report > span.short > span::text').extract_first()
        imdb = response.xpath(
            '//div[@id="info"]/span[contains(./text(), "IMDb")]/following-sibling::a/text()').extract_first()

        if not overview:
            overview = response.css('#link-report > span[property$=mary]::text').extract_first()
        directors = response.css('#info > span:nth-child(1) > span.attrs > a::text').extract()
        writers = response.css('#info > span:nth-child(3) > span.attrs>a::text').extract()
        casts = response.css('.attrs > a[rel$=starring]::text').extract()
        country = response.xpath(
            '//div[@id="info"]/span[contains(./text(), "制")]/following::text()[1]').extract_first().strip().split(" / ")
        lang = response.xpath(
            '//div[@id="info"]/span[contains(./text(), "语")]/following::text()[1]').extract_first().strip().split(" / ")

        small_image = response.meta.get("front_image_url", "")

        separator = title.find(' ')
        if separator != -1:
            subject_item['title'] = title[0:separator]
            subject_item['original_title'] = title[separator:]
        else:
            subject_item['title'] = title
            subject_item['original_title'] = ''

        subject_item['douban_link'] = response.url
        subject_item['year'] = get_num(year)
        subject_item['rating'] = rating
        subject_item['genres'] = genres
        subject_item['runtime'] = get_num(runtime)
        subject_item['release_at'] = get_date(release_at)
        subject_item['overview'] = overview
        subject_item['country'] = country
        subject_item['lang'] = lang
        subject_item['imdb'] = imdb

        subject_item['season_count'] = 0

        subject_item['directors'] = directors
        subject_item['writers'] = writers
        subject_item['casts'] = casts

        subject_item['small_image'] = small_image

        yield subject_item
