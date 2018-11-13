# encoding:utf-8
import requests
import psycopg2
from bs4 import BeautifulSoup

# 数据库连接参数
conn = psycopg2.connect(database="shennongjia", user="postgres", password="313616", host="127.0.0.1", port="5432")
cur = conn.cursor()

urls = ["https://lishi.tianqi.com/shennongjia/201810.html",
        "https://lishi.tianqi.com/shennongjia/201809.html",
        "https://lishi.tianqi.com/shennongjia/201808.html",
        "https://lishi.tianqi.com/shennongjia/201807.html",
        "https://lishi.tianqi.com/shennongjia/201806.html",
        "https://lishi.tianqi.com/shennongjia/201805.html",
        "https://lishi.tianqi.com/shennongjia/201804.html",
        "https://lishi.tianqi.com/shennongjia/201803.html",
        "https://lishi.tianqi.com/shennongjia/201802.html",
        "https://lishi.tianqi.com/shennongjia/201801.html",
        "https://lishi.tianqi.com/shennongjia/201712.html",
        ]
file = open("Shennongjia2.csv", 'w')
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    weather_list = soup.select('div[class="tqtongji2"]')
    for weather in weather_list:
        weather_date = weather.select('a')[0].string.encode('utf-8')

        ul_list = weather.select('ul')
        i = 0
        for ul in ul_list:
            li_list = ul.select('li')
            str = ""
            for li in li_list:
                str += li.string.encode('utf-8').decode() + ","

            if i != 0:
                file.write(str + '\n')
                date = li_list[0].string.encode('utf-8').decode()
                Maximum = li_list[1].string.encode('utf-8').decode()
                Minimum = li_list[2].string.encode('utf-8').decode()
                the_weather = li_list[3].string.encode('utf-8').decode()
                winddirection = li_list[4].string.encode('utf-8').decode()
                windpower = li_list[5].string.encode('utf-8').decode()
                # 插入数据 （特别注意只能用%s  不能用%d,数值型数据不用引号
                cur.execute("insert into weatherdate values(%s,%s,%s,%s,%s,%s)",
                            (date, Maximum, Minimum, the_weather, winddirection, windpower))
                conn.commit()  # 提交命令，否则数据库不执行插入操作

                print(str)
            i += 1
file.close()
cur.close()
conn.close()
