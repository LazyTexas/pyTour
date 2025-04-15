# 获取广东省行政区划

import requests
from bs4 import BeautifulSoup
import mysql.connector

base_url = 'https://baike.baidu.com/item/%E5%B9%BF%E4%B8%9C%E7%9C%81/132473'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 初始化一个空列表来存储行政区划
district = []

response = requests.get(base_url, headers=headers)

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(response.content, 'html.parser')

# 获取行政区划的table
table = soup.find('div', {"data-uuid": "t2RIovy4ymVQ"})

rows = table.find_all('tr')
count = 0
for row in rows:
    count+=1
    if count==1 or count==23:
        continue
    cols = row.find_all("td")
    cols = [col.text.strip() for col in cols]
    if len(cols)!=3:
        cols.append(cols[0])
    # district.append([cols[0],cols[2]])
    district.append({
        'city': cols[0],
         'county': cols[2]
         })

for i in district:
    print(i)

# 构造和mysql的连接
conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='123456',
            port=3306,
            charset='utf8',
            database='pytour'
        )
cursor = conn.cursor()
create = '''
CREATE TABLE district (
  `city` VARCHAR(50),
  `county` VARCHAR(50) primary key
);'''
cursor.execute(create)
conn.commit()
sql='''insert into `district` (`city`, `county`) VALUES (%s, %s);'''
for cities in district:
    counties=cities['county'].split('、')
    for county in counties:
        cursor.execute(sql, (cities['city'], county))
        conn.commit()
cursor.close()
conn.close()