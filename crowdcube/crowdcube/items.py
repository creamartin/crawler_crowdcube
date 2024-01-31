# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

class CommentItem(scrapy.Item):
    pitch = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=Join(),)
    id = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=Join(),)
    parent = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=Join(),)
    title = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=Join(),)
    author = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=Join(),)
    date = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=Join(),)
    replies = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=Join(),)
    content = scrapy.Field(input_processor=MapCompose(remove_tags,str.split),output_processor=Join(),)
