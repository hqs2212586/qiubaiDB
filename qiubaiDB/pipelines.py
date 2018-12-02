# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# Mysql版本
import pymysql

class QiubaiMysqlPipeline(object):
    conn = None    # 连接对象声明为全局属性
    cursor = None   # 游标对象
    def open_spider(self, spider):
        print("开始爬虫")
        # 连接数据库
        self.conn = pymysql.connect(host='127.0.0.1', port=3306,
                        user='root', password='1234', db='qiubai')

    def process_item(self, item, spider):
        """
        编写向数据库中存储数据的相关代码
        :param item:
        :param spider:
        :return:
        """
        # 1、连接数据库：open_spider()
        # 2、执行sql语句
        sql = 'insert into qiubai values("%s", "%s")' % (item['author'], item['content'])
        self.cursor = self.conn.cursor()  # 创建游标对象
        try:
            self.cursor.execute(sql)   # 执行sql语句
            # 3、提交事务
            self.conn.commit()
        except Exception as e:
            # 出现错误的时候：打印错误并回滚
            print(e)
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        print("爬虫结束")
        self.cursor.close()  # 关闭游标
        self.conn.close()    # 关闭连接对象

# redis版本
import redis
import json

class QiubaidbPipeline(object):
    conn = None   # 声明全局连接对象
    def open_spider(self, spider):
        print("开始爬虫")
        # 连接redis数据库
        self.conn = redis.Redis(host='127.0.0.1', port=6379)

    def process_item(self, item, spider):
        """编写向redis中存储数据的相关代码"""
        dic = {      # dic中封装item对象中获取的页面数据
            'author': item['author'],
            'content': item['content']
        }
        dic_str = json.dumps(dic)   # 转为字符串
        # redis数据库写入
        # lpush：从左往右添加元素。在key对应list的头部添加字符串元素
        self.conn.lpush('data', dic_str)  # 每一次获取的值追加到列表当中
        return item


# 文件保存
class QiubaiByFilesPipeline(object):
    """实现将数据值存储到本地磁盘中"""
    fp = None
    def open_spider(self, spider):
        print("开始爬虫")
        # 在该方法中打开文件
        self.fp = open('./qiubai_pipe.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 取出Item对象中存储的数据值
        author = item['author']
        content = item['content']
        # 持久化存储
        self.fp.write(author + ":" + content+ '\n\n\n')  # 写入数据
        return item

    def close_spider(self, spider):
        print("爬虫结束")
        # 关闭文件
        self.fp.close()



