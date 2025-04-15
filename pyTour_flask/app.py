from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

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

# 获取景点数据
def get_city(city):
    with conn.cursor() as cursor:
        sql = f"SELECT title, img, city, county, location, phrase, score, peopleCount, url, level, detail, time, pictures, price so FROM `{city}` order by peopleCount DESC;"
        cursor.execute(sql)
        results = cursor.fetchall()
    data_list = []
    for result in results:
        data = {
            'title': result[0],
            'img': result[1],
            'city': result[2],
            'county': result[3],
            'location': result[4],
            'phrase': result[5],
            'price': result[13],
            'score': result[6],
            'peopleCount': result[7],
            'url': result[8],
            'level': result[9],
            'detail': result[10],
            'time': result[11],
            'pictures': result[12]
        }
        data_list.append(data)
    return data_list

def get_district(city_district):
    with conn.cursor() as cursor:
        sql = f"SELECT county FROM `district` where city='{city_district}';"
        cursor.execute(sql)
        results = cursor.fetchall()
    data_list = []
    for result in results:
        data = {
            'city': city_district,
            'county': result[0]
        }
        data_list.append(data)
    return data_list

def get_pie_data(city):
    with conn.cursor() as cursor:
        sql=f'SELECT county, COUNT(*) FROM `{city}` GROUP BY county ORDER BY COUNT(*) DESC;'
        cursor.execute(sql)
        results = cursor.fetchall()
    data_list = []
    for result in results:
        data = {
            'county': result[0],
            'count': result[1]
        }
        data_list.append(data)
    return data_list

def get_bar_data(city):
    with conn.cursor() as cursor:
        sql=f'''-- 创建虚拟区间表
                WITH ranges AS (
                    SELECT '[1000,n)' AS price_range, 1000 AS range_start
                    UNION ALL SELECT '[900,1000)', 900
                    UNION ALL SELECT '[800,900)', 800
                    UNION ALL SELECT '[700,800)', 700
                    UNION ALL SELECT '[600,700)', 600
                    UNION ALL SELECT '[500,600)', 500
                    UNION ALL SELECT '[400,500)', 400
                    UNION ALL SELECT '[300,400)', 300
                    UNION ALL SELECT '[200,300)', 200
                    UNION ALL SELECT '[100,200)', 100
                    UNION ALL SELECT '[0,100)', 0
                )
                
                -- 查询并左连接
                SELECT
                    ranges.price_range,
                    IFNULL(COUNT(`{city}`.price), 0) AS count
                FROM ranges
                LEFT JOIN (
                    SELECT
                        CASE
                            WHEN price >= 1000 THEN '[1000,n)'
                            WHEN price >= 900 THEN '[900,1000)'
                            WHEN price >= 800 THEN '[800,900)'
                            WHEN price >= 700 THEN '[700,800)'
                            WHEN price >= 600 THEN '[600,700)'
                            WHEN price >= 500 THEN '[500,600)'
                            WHEN price >= 400 THEN '[400,500)'
                            WHEN price >= 300 THEN '[300,400)'
                            WHEN price >= 200 THEN '[200,300)'
                            WHEN price >= 100 THEN '[100,200)'
                            WHEN price >= 0 THEN '[0,100)'
                        END AS price_range,
                        price
                    FROM `{city}`
                ) AS `{city}`
                ON ranges.price_range = `{city}`.price_range
                GROUP BY ranges.price_range, ranges.range_start
                ORDER BY ranges.range_start ASC;'''
        cursor.execute(sql)
        results = cursor.fetchall()
    data_list = []
    for result in results:
        data = {
            'interval': result[0],
            'count': result[1]
        }
        data_list.append(data)
    return data_list

# 定义根路由
@app.route('/')
def index():
    return render_template('index.html')

# 转到城市详细界面
@app.route('/city-detail')
def city_detail():
    city = request.args.get('city')  # 获取 URL 参数
    return render_template('city-detail.html', city=city)

# 景点数据 API
@app.route('/api/get-city')
def attractions_api():
    city = request.args.get('city')  # 从 URL 参数中获取 city
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    attractions = get_city(city)
    return jsonify(attractions)

# 行政区划 API
@app.route('/api/get-district')
def district_api():
    city_district = request.args.get('city')  # 从 URL 参数中获取 city
    if not city_district:
        return jsonify({"error": "City parameter is required"}), 400
    district = get_district(city_district)
    return jsonify(district)

# 玫瑰图可视化数据 API
@app.route('/api/get-pie-data')
def pie_data_api():
    city = request.args.get('city')  # 从 URL 参数中获取 city
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    data = get_pie_data(city)
    return jsonify(data)

# 柱状图可视化数据 API
@app.route('/api/get-bar-data')
def data_api():
    city = request.args.get('city')  # 从 URL 参数中获取 city
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    data = get_bar_data(city)
    return jsonify(data)



# 运行应用程序
if __name__ == '__main__':
    app.run(debug=True)