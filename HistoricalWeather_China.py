# from xpinyin import Pinyin
# pin = Pinyin()
# test2 = pin.get_pinyin("大河向东流", "")
# print(test2)
################################################################
# encoding:utf-8
import requests
import psycopg2
from bs4 import BeautifulSoup
# 数据库连接参数
conn = psycopg2.connect(database="historicalweather", user="postgres", password="313616", host="127.0.0.1", port="5432")
cur = conn.cursor()
target_year_list = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
target_month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]


def get_urls(city_pinyin):
    urls = []

    for year in target_year_list:
        for month in target_month_list:
            date = year + month
            urls.append("http://lishi.tianqi.com/{}/{}.html".format(city_pinyin, date))

    return urls


def get_city_dict(file_path):
    city_dict = {}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.replace("\n", "")
            city_name = line.split(" ")[0]
            city_pinyin = (line.split(" ")[1]).lower()

            ## 赋值到字典中...
            city_dict[city_pinyin] = city_name

    return city_dict


# =============================================================================
# main
# =============================================================================

file_path = "./city_pinyin_list.txt"
city_dict = get_city_dict(file_path)

for city in city_dict.keys():
    urls = get_urls(city)
    # print(urls)
    # print(city)
    for url in urls:
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
                    cur.execute("insert into historicalweather values(%s,%s,%s,%s,%s,%s,%s)",
                                (date, Maximum, Minimum, the_weather, winddirection, windpower, city))
                    conn.commit()  # 提交命令，否则数据库不执行插入操作
                i += 1
