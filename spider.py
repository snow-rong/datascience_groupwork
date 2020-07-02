import requests
import bs4
import random
import pandas as pd
import time
from openpyxl import load_workbook
from fake_useragent import UserAgent


def downloadPage(url):
    # 下载页面方法，用requests模块，使用代理，避免重复请求次数过多；多开几个进程，加快下载速度
    ua = UserAgent()
    headers = {
        'Connection': 'close',
        'Content-Type': 'text/html; charset=utf-8',
        'User-Agent': ua.random}  # 随机生成浏览器的请求头
    try:
        data = requests.get(url, headers=headers).text
        return data
    except BaseException:

        if (url in errordic):
            errordic[url] = errordic[url] + 1
        else:
            errordic[url] = 1
        if (errordic[url] < 4):
            print(url + '【第】' + str(errordic[url]) + '次重试】')
            return downloadPage(url)
        else:
            print(url + '【下载页面失败】')
            return ''


def get_region(url):
    # 得到各区的url链接及区名
    region_list = []
    response = downloadPage(url)
    bsoup = bs4.BeautifulSoup(response, 'lxml')
    region = bsoup.find('div', class_='items').find('span', class_='elems-l').find_all('a')
    for i in region:
        name = i.get_text()
        href = i.attrs['href']
        region_list.append({'href': href, 'name': name})
    return region_list


def get_info(url, name, writer):
    # 获取该区域二手房的信息数据
    print("--------------------------------------%s-------------------------------" % name)
    house_info = []
    for i in range(1, 21):

        url = url + "p" + str(i) + "#filtersort"
        print("开始爬取安居客平台北京%s二手房第%s页信息....." % (name, str(i)))
        response = downloadPage(url)
        # 生成bs4对象
        bsoup = bs4.BeautifulSoup(response, 'lxml')

        house_list = bsoup.find_all('li', class_="list-item")

        for house in house_list:
            # bs4解析文件
            titile = house.find('a').text.strip()


            house_type = house.find('div', class_='details-item').span.text  #房子标题

            house_area = house.find('div', class_='details-item').contents[3].text#获取面积

            house_floor = house.find('div', class_='details-item').contents[5].text#获取层数

            house_tags = house.find('div',class_='tags-bottom').text #获取房子标签
            tag_length =len(house_tags)
            if tag_length>1:
                #标签分割
                 tag_num=len(house.find('div',class_='tags-bottom'))
                 if tag_num==3:
                    tags_1 = house.find('div',class_='tags-bottom').contents[1].text
                    tags=tags_1
                 elif tag_num==4:
                    tags_1 = house.find('div', class_='tags-bottom').contents[1].text
                    tags_2 = house.find('div',class_='tags-bottom').contents[2].text
                    tags=tags_1+' '+tags_2
                 elif tag_num==5:
                    tags_1 = house.find('div', class_='tags-bottom').contents[1].text
                    tags_2 = house.find('div', class_='tags-bottom').contents[2].text
                    tags_3=house.find('div', class_='tags-bottom').contents[3].text
                    tags=tags_1+' '+tags_2+' '+tags_3
            else:
                tags='NAN'

            address = house.find('span', class_='comm-address').text.strip()#获取地址

            price = house.find('span', class_='price-det').text.strip()#获取房子总价

            unit_price = house.find('span', class_='unit-price').text.strip()#获取每平方米的价格

            length = len(house.find('div', class_='details-item'))
            if length==9:
                build_time=house.find('div', class_='details-item').contents[7].text   #获取建造时间
            else:
                build_time='NAN'
            pd1 = pd.DataFrame({'titile': titile, 'house_type': house_type, 'build_area': house_area,
                                'bulid_floor': house_floor, 'address': address, 'price': price,
                                'unit_price': unit_price,'build_time':build_time,'house_tags':tags},index=[0])
            house_info.append(pd1)

        second = random.randrange(4, 5)  # 每次访问间隔4到5秒，防止网页要求验证
        time.sleep(second)

    house_info2 = pd.concat(house_info)
    return house_info2


# print(type(house_info2))
#  house_info2.to_excel(writer,sheet_name=name)
#   writer.save()
#  writer.close()

if __name__ == '__main__':
    url = 'https://beijing.anjuke.com/sale/'
    region_list = get_region(url)
    writer = pd.ExcelWriter(r'd:\\bj_house_info.xlsx')
    for dic in region_list:
        url = dic.get('href')
        name = dic.get('name')
        house_info = get_info(url, name, writer)
        house_info.to_excel(writer, sheet_name=name)
    writer.save()
    writer.close()
    print("爬取完毕")
