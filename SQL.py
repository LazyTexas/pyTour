import mysql.connector

# 构造和mysql的连接
conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='123456',
            port=3306,
            charset='utf8',
            database='pytour',
            buffered = True
        )
cursor = conn.cursor()
sel='''select city from district group by city;'''
cursor.execute(sel)
district=[city[0] for city in cursor.fetchall()]
conn.commit()
# print(district)
for city in district:
    create = f'''
    CREATE TABLE `{city}` (
      `title` TEXT,
      `img` TEXT,
      `city` VARCHAR(50),
      `county` VARCHAR(50),
      `location` TEXT,
      `peopleCount` INT,
      `score` FLOAT,
      `phrase` TEXT,
      `url` TEXT,
      `price` FLOAT,
      `level` TEXT,
      `detail` TEXT,
      `time` TEXT,
      `pictures` MEDIUMTEXT,
      `json` MEDIUMTEXT
    );'''
    cursor.execute(create)
    conn.commit()
cursor.close()
conn.close()