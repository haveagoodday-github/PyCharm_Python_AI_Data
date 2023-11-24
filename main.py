import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
import pymysql

# 连接数据库
try:
    connect = pymysql.connect(host='localhost', user='root', password='root', port=3306,
                              db='photoworldForPython',  # 指定数据库
                              autocommit=True,  # 自动提交到数据库
                              auth_plugin_map='mysql_native_password')
    print("Databases Connect Success")

    db = connect.cursor(pymysql.cursors.DictCursor)  # 创建游标，查询数据以字典形式返回，默认以元组形式返回
except:
    print("Databases Connect Error")


def insertData(title, item):
    mysqlStatement = '''
                INSERT INTO PageForImage (title, imgURL, content, tags, time, type, author, detailsURL)
                VALUES ('{title}', '{imgURL}', '{content}', '{tags}', '{time}', '{type}', '{author}', '{detailsURL}');
            '''.format(title=title,
                       imgURL=item['Image'],
                       content=item['Content'],
                       tags=','.join(item['Tag']),
                       time=item['Meta']['time'],
                       type=item['Meta']['type'],
                       author=item['Meta']['author'],
                       detailsURL=item['detailsURL'])
    db.execute(mysqlStatement)
    # print("Insert Data Success.", end="\n======" + title + "======\n")


os.makedirs('./images/', exist_ok=True)

# 将option作为参数添加到Chrome中
dr = webdriver.Chrome()
dr.implicitly_wait(10)  # 最大等待时间10秒(弹性等待)[全局]
dr.set_window_size(1920, 1080)
url = "https://www.photoworld.com.cn/"
dr.get(url)

dr.find_element(By.XPATH, "/html/body/div[1]/header/div/nav/ul/li[3]/a").click()  # 点击“影像”
maxPageNumber = dr.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/nav/div/a[3]").text  # 获取最大页数
pageData = []

for page in range(0, int(maxPageNumber)):
    data = {}
    group = dr.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/article")
    # 遍历元素列表并将数据添加到字典中
    for item in group:
        title = item.find_element(By.CLASS_NAME, "big-thumb-title").text
        try:
            image = item.find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            image = "Null"
        content = item.find_element(By.CLASS_NAME, "big-thumb-excerpt").text
        tag = [temp.text for temp in item.find_element(By.CLASS_NAME, "tag").find_elements(By.TAG_NAME, "a")]
        time = item.find_element(By.TAG_NAME, "aside").find_element(By.TAG_NAME, "time").text
        type = item.find_element(By.TAG_NAME, "aside").find_element(By.CLASS_NAME, "recent-cat").text
        author = item.find_element(By.TAG_NAME, "aside").find_element(By.CLASS_NAME, "recent-author").text
        detailsURL = item.find_element(By.CLASS_NAME, "big-thumb-title").find_element(By.TAG_NAME, "a").get_attribute(
            "href")
        data[title] = {
            "Image": image,
            "Content": content,
            "Tag": tag,
            "Meta": {
                "time": time,
                "type": type,
                "author": author
            },
            "detailsURL": detailsURL
        }
    # 打印数据
    for title, item in data.items():
        print(f"Title: {title}")
        # print(item)
    pageData.append(data)
    if page >= int(maxPageNumber):
        break
    dr.find_element(By.CLASS_NAME, "next").click()  # Next
    print("========================================{}========================================".format(page + 1),
          end="\n")

for pageItem in pageData:
    for title, item in pageItem.items():
        # print(f"Title: {title}")
        # print(item)
        insertData(title, item) # 存储数据


db.close()  # 关闭数据库