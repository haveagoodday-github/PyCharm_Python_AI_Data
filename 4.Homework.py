from selenium import webdriver
from selenium.webdriver.common.by import By
import pymongo

dr = webdriver.Chrome()
dr.implicitly_wait(10)
dr.set_window_size(1920, 1080)
url = "http://www.ptpress.com.cn/"
dr.get(url)

group = dr.find_elements(By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div[2]/ul/li')
contents = []
for item in group:
    temp = item.find_element(By.CLASS_NAME, 'name').text
    contents.append(temp)

print(contents)

client = pymongo.MongoClient('localhost', 27017)
db = client.mydatabase  # 数据库名称
collection = db.mycollection  # 集合名称
for content in contents:
    data = {"title": content}
    collection.insert_one(data)
