# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import csv
import mysql.connector
import os

class ExcelPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active
        self.sheet.title = 'pyTour'
        # self.sheet.append(['景点名称','景点图片','city','county','景点地址','景点参观人数','景点评分','景点短语','景点链接','景点最低价格','景点等级','景点详细信息','景点开放时间','景点图片合集','json'])
        self.sheet.append(
            ['景点名称', '景点图片', '景点地址', '景点参观人数', '景点评分', '景点短语', '景点链接',
             '景点最低价格', '景点等级', '景点详细信息', '景点开放时间', '景点图片合集', 'json'])

    # 打开爬虫时调用
    def open_spider(self, spider):
        pass

    # 关闭爬虫调用
    def close_spider(self, spider):
        self.wb.save('test.xlsx')

    # 每次拿到数据时调用
    def process_item(self, item, spider):
        # self.sheet.append([item['title'],item['img'],item['city'],item['county'],item['location'],item['peopleCount'],item['score'],item['phrase'],item['url'],item['price'],item['level'],item['detail'],item['time'],item['pictures'],item['json']])
        self.sheet.append(
            [item['title'], item['img'], item['location'], item['peopleCount'],
             item['score'], item['phrase'], item['url'], item['price'], item['level'], item['detail'], item['time'],
             item['pictures'], item['json']])
        return item

class CsvPipeline:
    def __init__(self):
        self.file = open('test.csv', 'w', newline='', encoding='utf-8')
        self.csvwriter = csv.writer(self.file)
        self.csvwriter.writerow(['景点名称','景点图片','city','county','景点地址','景点参观人数','景点评分','景点短语','景点链接','景点最低价格','景点等级','景点详细信息','景点开放时间','景点图片合集','json'])
        self.name = ''

    # 打开爬虫时调用
    def open_spider(self, spider):
        pass

    # 关闭爬虫调用
    def close_spider(self, spider):
        self.file.close()
        os.rename('test.csv',f'{self.name}.csv')

    # 每次拿到数据时调用
    def process_item(self, item, spider):
        self.name=item['city']
        self.csvwriter.writerow([item['title'],item['img'],item['city'],item['county'],item['location'],item['peopleCount'],item['score'],item['phrase'],item['url'],item['price'],item['level'],item['detail'],item['time'],item['pictures'],item['json']])
        return item

class MysqlPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='123456',
            port=3306,
            charset='utf8',
            database='pytour',
            buffered=True
        )
        self.cursor = self.conn.cursor()

    # 打开爬虫时调用
    def open_spider(self, spider):
        pass

    # 关闭爬虫调用
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    # 每次拿到数据时调用
    def process_item(self, item, spider):
        sql = f'''insert into `{item['city']}` (`title`,`img`,`city`,`county`,`location`,`peopleCount`,`score`,`phrase`,`url`,`price`,`level`,`detail`,`time`,`pictures`,`json`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        self.cursor.execute(sql, (item['title'],item['img'],item['city'],item['county'],item['location'],item['peopleCount'],item['score'],item['phrase'],item['url'],item['price'],item['level'],item['detail'],item['time'],item['pictures'],item['json']))
        self.conn.commit()
        return item