# encoding:utf-8
import requests
import psycopg2
from bs4 import BeautifulSoup
# 数据库连接参数
conn = psycopg2.connect(database="shennongjia", user="postgres", password="313616", host="127.0.0.1", port="5432")
cur = conn.cursor()
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
years = ['11', '12', '13', '14', '15', '16', '17', '18']
for year in years:
    for month in months:
        url = "https://lishi.tianqi.com/shennongjia/20" + year + month + ".html"
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        weather_list = soup.select('div[class="tqtongji2"]')
        for weather in weather_list:
            ul_list = weather.select('ul')
            i = 0
            for ul in ul_list:
                li_list = ul.select('li')
                if i != 0:
                    if li_list[0].string:
                        date = str(li_list[0].string.encode('utf-8').decode())
                    if li_list[1].string:
                        Maximum = str(li_list[1].string.encode('utf-8').decode())
                    if li_list[2].string:
                        Minimum = str(li_list[2].string.encode('utf-8').decode())
                    if li_list[3].string:
                        the_weather = str(li_list[3].string.encode('utf-8').decode())
                    if li_list[4].string:
                        winddirection = str(li_list[4].string.encode('utf-8').decode())
                    if li_list[5].string:
                        windpower = str(li_list[5].string.encode('utf-8').decode())
                    # 插入数据 （特别注意只能用%s  不能用%d,数值型数据不用引号
                    cur.execute("insert into weatherdata values(%s,%s,%s,%s,%s,%s)",
                                (date, Maximum, Minimum, the_weather, winddirection, windpower))
                    conn.commit()  # 提交命令，否则数据库不执行插入操作
                i += 1
# file.close()
cur.close()
conn.close()
