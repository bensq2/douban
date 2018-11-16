# -*- coding: utf-8 -*-
import pymongo
from douban.settings import mongo_host,mongo_port
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#需要开启pipelines
class DoubanPipeline(object):
    def __init__(self):
        host=mongo_port
        port=mongo_port
        client=pymongo.MongoClient(host=host,port=port)
        mydb=client['a']
        self.post=mydb['collect']
       #item 来自爬取到的数据
    def process_item(self, item, spider):
        data=dict(item)
        self.post.insert(data)
        return item
