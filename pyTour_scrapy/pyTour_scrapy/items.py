# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# ['景点名称', '景点图片', 'city', 'county', '景点地址', '景点参观人数', '景点评分', '景点短语', '景点链接','景点最低价格', '景点等级', '景点详细信息', '景点开放时间', '景点图片合集', 'json']
# [item['title'], item['img'], item['city'], item['county'], item['location'], item['peopleCount'],item['score'], item['phrase'], item['url'], item['price'], item['level'], item['detail'], item['time'],item['pictures'], item['json']]
import scrapy

class PyTourItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title =  scrapy.Field()
    img = scrapy.Field()
    location = scrapy.Field()
    phrase = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    level = scrapy.Field()
    detail = scrapy.Field()
    time = scrapy.Field()
    peopleCount = scrapy.Field()
    score = scrapy.Field()
    pictures = scrapy.Field()
    json = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()