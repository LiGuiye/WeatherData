# 神农架一周天气预测
# encoding:utf-8
import requests
import psycopg2
from bs4 import BeautifulSoup
import re
# 数据库连接参数
conn = psycopg2.connect(database="shennongjia", user="postgres", password="313616", host="127.0.0.1", port="5432")
cur = conn.cursor()

url = "https://www.tianqi.com/shennongjia/7/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
WeatherToday = soup.select('div[class="tit_img01"]')
WeatherToday2 = soup.p.text.replace('<p>', '')
print(WeatherToday2)
# 导入数据库存在问题
# cur.execute("insert into reminder(report) values (%s);", "WeatherToday2")
# conn.commit()  # 提交命令，否则数据库不执行插入操作

weather_list = soup.select('div[class="weatherbox2"]')
for weather in weather_list:
    dl_list = weather.select('dl')
    i = 0
    while i < 13:
        dd_list = dl_list[i].select('dd')
        # print(dd_list)
        date = str(dl_list[i+1].string.encode('utf-8').decode())
        print("date::::" + date)
        if dd_list[0].string:
            week = str(dd_list[0].string.encode('utf-8').decode())
            print("week::::" + week)
        if dd_list[1].string:
            air = str(dd_list[1].string.encode('utf-8').decode())
            print("air::::" + air)
        if dd_list[3].string:
            rain = str(dd_list[3].string.encode('utf-8').decode())
            print("rain::::" + rain)
        if str(dd_list[4]):
            temp = str(dd_list[4])
            # 利用正则表达式消除标签
            dr = re.compile(r'<[^>]+>', re.S)
            dd = dr.sub('', str(temp))
            print("temp:::::"+dd)
        if dd_list[5].string:
            wind = str(dd_list[5].string.encode('utf-8').decode())
            print("wind::::" + wind)

        # 插入数据 （特别注意只能用%s  不能用%d,数值型数据不用引号
        cur.execute("insert into weatherforecast values(%s,%s,%s,%s,%s,%s)", (date, week, air, rain, dd, wind))
        conn.commit()  # 提交命令，否则数据库不执行插入操作
        i = i + 2
        print("//////")

cur.close()
conn.close()
