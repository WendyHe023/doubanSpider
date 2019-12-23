# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanPipeline(object):

    def process_item(self, item, spider):
        return item


class ElasticSearchPipeline(object):

    # 将数据写入es中
    def process_item(self, item, spider):
        item.save_to_es()
        return item
