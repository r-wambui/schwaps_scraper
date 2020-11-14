# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

from datetime import datetime
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class CookcountyPipeline:
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline(object):

    def __init__(self):
         self.parcel_seen = set()

    def process_item(self, item, spider):
        if spider.name == "property_v2":
            if item['PARCEL_NUMBER'] in self.parcel_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.parcel_seen.add(item['PARCEL_NUMBER'])
                return item 
        else:
            return item 


# class HtmlFilePipeline(object):
#     def process_item(self, item, spider):
#         if spider.name == "calendar":
#             date = datetime.now().strftime("%Y-%m-%d %H:%M")
#             file_name = hashlib.sha224(date.encode()).hexdigest()
#             with open('files/%s.html' % file_name, 'w+b') as f:
#                 f.write(item['html'])
#             return item
        
