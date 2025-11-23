# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FileInfoItem(scrapy.Item):
    # 定义你的item字段，就像你在代码中使用的字典键一样
    file_name = scrapy.Field()        # 文件名
    local_path = scrapy.Field()       # 本地存储路径
    remote_path = scrapy.Field()      # 远程路径
    file_metadata = scrapy.Field()    # 文件元数据
    other_metadata = scrapy.Field()   # 其他元数据（字典）
