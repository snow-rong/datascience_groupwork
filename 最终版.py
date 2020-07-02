import requests
import bs4
import time
import random
import pandas as pd
import openpyxl
house_info=[]
quyu=['chaoyang','haidian','dongchenga','xicheng','fengtai','tongzhou','shijingshan','changoing','daxing','shunyi','fangshan','mentougou','miyun','huairou','pinggua','yanqing','beijngzhoubiana']
for j in quyu:
    for i in range(1,20):
        url="https://beijing.anjuke.com/sale/"+j+"/p"+str(i)+"/#filtersort"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 "
        }
        print("开始爬取安居客平台北京"+j+"二手房第%s页信息....." %(str(i)))
        response = requests.get(url=url, headers=headers)
        #生成bs4对象
        bsoup=bs4.BeautifulSoup(response.text,'lxml')

        house_list=bsoup.find_all('li', class_="list-item")

        for house in house_list:
         #bs4解析文件
            titile = house.find('a').text.strip()
            house_type = house.find('div', class_='details-item').span.text
            buid_time = house.find('div', class_='details-item').contents.text
            area = house.find('div', class_='details-item').contents[3].text
            address = house.find('span', class_='comm-address').text.strip()
            price = house.find('span', class_='price-det').text.strip()
            unit_price = house.find('span', class_='unit-price').text.strip()

            pd1= pd.DataFrame({'titile': titile, 'house_type': house_type,'build_time': buid_time,
                 'area': area, 'address': address, 'price': price, 'unit_price': unit_price},index=[0])
            house_info.append(pd1)
        second=random.randrange(3,5)
        time.sleep(second)

    house_info2=pd.concat(house_info)
    house_info2.to_excel(j+'.xlsx',index=False)
