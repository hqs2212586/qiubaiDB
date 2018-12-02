# -*- coding: utf-8 -*-
import scrapy
from qiubaiDB.items import QiubaidbItem


class QiubaimysqlSpider(scrapy.Spider):
    name = 'qiubaiMysql'
    # allowed_domains = ['www.qiushibaike.com/text']  # 图片等信息可能不属于指定域名之下
    start_urls = ['https://www.qiushibaike.com/text/']  # 注意修改默认协议头

    def parse(self, response):
        # 段子的内容和作者
        div_list = response.xpath('//div[@id="content-left"]/div')  # 使用xpath来执行指定内容的解析

        for div in div_list:
            # 通过xpath解析到的指定内容被存储到了selector对象中
            # 需要通过extract()方法来提取selector对象中存储的数据值
            author = div.xpath('./div/a[2]/h2/text()').extract_first()   # './'表示解析当前局部div; a[2]表示第二个a标签
            content = div.xpath('.//div[@class="content"]/span/text()').extract_first()  # './/'表示当前局部所有元素；@class匹配类属性

            # 创建item对象
            item = QiubaidbItem()
            # 数据值写入item对象中
            item['author'] = author
            item['content'] = content

            # 提交给管道(循环几次就提交几次)
            yield item
