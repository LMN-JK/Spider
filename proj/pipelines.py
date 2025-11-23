# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import pymysql
from twisted.enterprise import adbapi
from itemadapter import ItemAdapter


class MySQLAsyncPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 类方法，Scrapy会使用它来创建pipeline实例
        # 从settings.py中读取数据库配置
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )
        # 创建数据库连接池
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用连接池进行异步的数据库插入操作
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 可以添加错误处理回调
        query.addErrback(self.handle_error, item, spider)
        return item

    def do_insert(self, cursor, item):
        insert_sql = """
        INSERT INTO regulations 
        (publish_date, title, issuing_authority, document_number, is_valid, category, source_url, other_metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
        values = (
        item['file_metadata']['publish_date'],
        item['file_metadata']['title'],
        item['file_metadata']['issuing_authority'],
        item['file_metadata']['document_number'],
        item['file_metadata']['is_valid'],
        item['other_metadata']['category'],  # 例如，category现在被认为是动态元数据之一
        item['other_metadata']['source_url'],
        json.dumps(item['other_metadata'], ensure_ascii=False)  # 序列化为JSON字符串
        )
        try:
            cursor.execute(insert_sql, values)
            # 使用连接池时不需要手动commit，Twisted会处理[1,4](@ref)
        except Exception as e:
            # 错误处理逻辑，例如记录日志或忽略重复项
            if "Duplicate" in repr(e):
                # 处理重复数据，例如跳过
                pass
            else:
                print(f"插入数据库时发生错误: {e}")
                # 可以选择重新抛出异常，让Scrapy处理
                raise

    def handle_error(self, failure, item, spider):
        # 处理插入时可能发生的错误
        spider.logger.error("Error inserting item %s: %s" % (item['file_metadata']['title'], failure))