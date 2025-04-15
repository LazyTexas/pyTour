from typing import Iterable

from scrapy import cmdline

if __name__ == '__main__':
    # run=input()
    # Scrapy的暂停与重启
    # run="scrapy crawl pyTour_spider -o test.csv -s JOBDIR=JOBDIR"
    run="scrapy crawl pyTour_spider -s JOBDIR=JOBDIR"
    cmdline.execute(run.split())

import scrapy
import json
from ..items import PyTourItem
from scrapy import Selector, Request
from scrapy.http import HtmlResponse
import mysql.connector
import urllib.parse

class PyTourSpider(scrapy.Spider):
    name = "pyTour_spider"
    allowed_domains = ["piao.qunar.com"]
    start_urls=[]
    # 构造和mysql的连接
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='123456',
        port=3306,
        charset='utf8',
        database='pytour',
        buffered=True
    )
    cursor = conn.cursor()
    city=input('请输入城市:')
    select = f'''select county from district where city like '%{city}%';'''
    cursor.execute(select)
    counties = [county[0] for county in cursor.fetchall()]
    for county in counties:
        start_urls.append(f'https://piao.qunar.com/ticket/list.htm?keyword={urllib.parse.quote(county)}&region=&from=mpl_search_suggest&page=1')

    # start_urls = ["https://piao.qunar.com/ticket/list.htm?keyword=%E6%B8%85%E6%96%B0%E5%8C%BA&region=&from=mpl_search_suggest&page=1"]  # 清远市清新区
    # start_urls = ["https://piao.qunar.com/ticket/list.htm?keyword=%E8%BF%9E%E5%B7%9E%E5%B8%82&region=&from=mpl_search_suggest&page=1"]  # 清远市连州市
    # tail_urls = "&region=&from=mpl_search_suggest&page="

    # last_page=parse_page()
    # def start_requests(self):
    #     for page in last_page:
    #         yield Request(url=f"https://piao.qunar.com/ticket/list.htm?keyword=%E8%BF%9E%E5%B7%9E%E5%B8%82&region=&from=mpl_search_suggest&page={page}")

    # def start_requests(self):
    #     # 构造和mysql的连接
    #     conn = mysql.connector.connect(
    #         host='localhost',
    #         user='root',
    #         passwd='123456',
    #         port=3306,
    #         charset='utf8',
    #         database='pytour',
    #         buffered=True
    #     )
    #     cursor = conn.cursor()
    #     sel = '''select city from district group by city;'''
    #     cursor.execute(sel)
    #     district = [city[0] for city in cursor.fetchall()]
    #     conn.commit()
    #     for city in district:
    #         select = f'''select county from district where city='{city}';'''
    #         cursor.execute(select)
    #         counties = [county[0] for county in cursor.fetchall()]
    #         for county in counties:
    #             url=f'https://piao.qunar.com/ticket/list.htm?keyword={urllib.parse.quote(county)}&region=&from=mpl_search_suggest&page=1'
    #             yield Request(url=url,cb_kwargs={'city': city,'county': county})
    #             break
    #         break

    # 爬取最大页数，判断是否多页爬取
    def parse(self, response:HtmlResponse,  **kwargs):
        # print('parse')
        # 检测是否有数据，没有数据再次执行
        if response.text:
            select = Selector(response)
            # max_page=int(select.xpath('//*[@id="pager-container"]/div/a/text()').getall()[-2] or -1)
            page = select.xpath('//*[@id="pager-container"]/div/a/text()').getall()
            if page:
                max_page=int(page[-2])
                print("最大页数：",max_page)
                for i in range(1,max_page+1):
                    new_url=response.url[:-1]+str(i)
                    yield Request(url=new_url,callback=self.parse_item,dont_filter=True)
            else:
                print("最大页数： 1")
                yield Request(url=response.url,callback=self.parse_item,dont_filter=True)
        else:
            # 重新请求
            yield Request(url=response.url,callback=self.parse,dont_filter=True)

    # 通过parse_item,parse_detail,parse_score爬取景点信息
    def parse_item(self, response:HtmlResponse, **kwargs):
        # city = kwargs['city']
        # county = kwargs['county']
        # 检测是否有数据，没有数据再次执行
        if response.text:
            print("正在爬取...", response.url)
            select = Selector(response)
            list_items = select.xpath('//*[@id="search-list"]/div[@mp-role="sightItem"]')
            # print(response.text)
            # print("=======================================================================================================")
            # max_page = int(select.xpath('//*[@id="pager-container"]/div/a/text()').getall()[-2] or -1)
            # print(max_page)
            for list_item in list_items:
                pyTour_item = PyTourItem()
                # 所在地级市
                pyTour_item['city'] = self.city
                # 所在区、县（市）
                pyTour_item['county'] = list_item.xpath('//*[@id="searchValue"]/@value').get()
                # 景点名称
                pyTour_item['title'] = list_item.xpath('./@data-sight-name').get() or 'N/A'
                # 景点图片
                pyTour_item['img'] = list_item.xpath('./@data-sight-img-u-r-l').get() or 'N/A'
                # 景点地址
                pyTour_item['location'] = list_item.xpath('./@data-address').get() or 'N/A'
                # 景点短语
                pyTour_item['phrase'] = list_item.xpath('.//div[@class="intro color999"]/text()').get() or 'N/A'
                # 景点链接
                pyTour_item['url'] = "https://piao.qunar.com" + list_item.xpath('.//a[@class="name"]/@href').get() or 'N/A'
                # 景点最低价格
                pyTour_item['price'] = float(list_item.xpath('.//em/text()').get() or -1)
                # 景点等级
                pyTour_item['level'] = list_item.xpath('.//span[@class="level"]/text()').get() or 'N/A'
                # 跳转到景点链接进行下一步爬取
                detail_url = "https://piao.qunar.com" + list_item.xpath('.//a[@class="name"]/@href').get()
                yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': pyTour_item},dont_filter=True)
                # break
        else:
            # 重新请求
            yield Request(url=response.url, callback=self.parse_item, dont_filter=True)

    def parse_detail(self, response:HtmlResponse, **kwargs):
        pyTour_item = kwargs['item']
        # 检测是否有数据，没有数据再次执行
        if response.text:
            # print(response.text)
            sel = Selector(response)
            # 景点详细信息
            temp=sel.xpath('//*[@id="mp-charact"]/div[1]/div[1]/div[1]/p/text()').getall() or 'N/A'
            detail=''
            for i in temp:detail=detail+i
            pyTour_item['detail']=detail.strip()
            # pyTour_item['detail']=(sel.xpath('//*[@id="mp-charact"]/div[1]/div[1]/div[1]/p/text()').getall() or 'N/A').strip()
            # 景点开放时间
            pyTour_item['time']=(sel.xpath('//*[@id="mp-charact"]/div[1]/div[2]/div/div[2]/p/text()').get() or 'N/A').strip()
            # 景点图片合集
            pictures=sel.xpath('//*[@id="mp-slider-content"]/div/img/@src').getall()  or ['N/A']
            pyTour_item['pictures'] = '〇'.join(pictures)
            # 跳转到评论json获取json、评分和参观人数
            sightId_url="https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId="+sel.xpath('//*[@id="mp-tickets"]/@data-sightid').get()+"&index=1&page=1&pageSize=10&tagType=0"
            yield Request(url=sightId_url, callback=self.parse_score, cb_kwargs={'item': pyTour_item},dont_filter=True)
        else:
            # 重新请求
            yield Request(url=response.url, callback=self.parse_detail, dont_filter=True, cb_kwargs={'item': pyTour_item})


    def parse_score(self, response:HtmlResponse, **kwargs):
        pyTour_item = kwargs['item']
        # 检测是否有数据，没有数据再次执行
        if response.text:
            rs=json.loads(response.text)
            # 评论json字典
            pyTour_item['json']=json.dumps(rs) or 'N/A'
            # print(rs)
            # 景点参观人数
            pyTour_item['peopleCount'] = int(rs['data']['commentCount'] or -1)
            # 景点评分
            pyTour_item['score'] = float(rs['data']['score'] or -1)
            yield pyTour_item
        else:
            # 重新请求
            yield Request(url=response.url, callback=self.parse_score, dont_filter=True, cb_kwargs={'item': pyTour_item})

