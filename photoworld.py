"""
‼️ In case you're using Python 3.6 or an earlier version, stick with 13.8.6 ‼️
1、导入依赖
    pip install scrapy pymysql django mysqlclient
2、Django 使用方法
    创建Django项目
        django-admin startproject myproject
    创建应用程序
        python manage.py startapp myapp
    创建模型
        python manage.py makemigrations
        python manage.py migrate
    运行开发服务器
        cd myproject
        python manage.py runserver
3、scrapy 使用方法
    scrapy startproject photoworldProject
    scrapy genspider photoworld https://www.photoworld.com.cn/category/images
    scrapy runspider photoworld.py
"""

import scrapy
import pymysql
import time

# 数据库信息
global_username = "root"
global_password = "root"
# TODO: create database photoworldForPython
global_db = "photoworldForPython"  # 数据库名称
global_table_name = "PageForImage"

class SpiderNameSpider(scrapy.Spider):
    text_color = '\33[96m'
    name = 'photoworld'
    allowed_domains = ["www.photoworld.com.cn"]
    start_urls = ['https://www.photoworld.com.cn/category/images']
    # start_urls = [f'https://www.photoworld.com.cn/category/images/page/{i}' for i in range(1, 12)]

    def __init__(self, *args, **kwargs):
        super(SpiderNameSpider, self).__init__(*args, **kwargs)
        # 在Spider实例化时初始化数据库连接
        global global_username
        global global_password
        global global_db
        global global_table_name
        self.model = MySQLDatabase(user=global_username, password=global_password, db=global_db, table_name=global_table_name)

    def parse(self, response):
        page_max_num = int(response.xpath('//div[@class="nav-links"]/a/text()').getall()[-2])
        urls = [f'https://www.photoworld.com.cn/category/images/page/{i}' for i in range(1, page_max_num + 1)]
        print(f'{self.text_color}length: {len(urls)}')
        for index, url in enumerate(urls):
            yield scrapy.Request(url=url, callback=self.parseFunction)

        search_title = input("请通过标题搜索内容：")
        search_result = [i['title'] for i in self.model.search_by_title(search_title)]
        print(f'搜索结果数量: {len(search_result)}条, \n{search_result}')
        # TODO: For Test
        # yield scrapy.Request(url="https://www.photoworld.com.cn/category/images", callback=self.parseFunction)
        pass

    def parseFunction(self, response):
        replaceNT = lambda content: content.replace("\n", "").replace("\t", "")

        articles = response.xpath('//div[@id="cat-images-main"]//article')
        # for index, item in enumerate(articles):
        for index, item in enumerate(articles):
            link = replaceNT(item.xpath('.//h3/a/@href').get())  # 使用相对路径
            title = replaceNT(item.xpath('.//h3/a/text()').get())
            content = replaceNT(item.xpath('.//p[@class="excerpt big-thumb-excerpt"]/text()').get())
            imgurl = item.xpath('.//div/a/img[@class="wp-post-image"]/@src').get()
            tags = item.xpath('.//p[last()]/a/text()').getall()
            recent_time = [item.xpath('.//aside/time/@datetime').get(),
                           replaceNT(item.xpath('.//aside/time//text()').get())]
            recent_cat = item.xpath('.//aside/span[@class="recent-cat"]/a/text()').get()
            recent_author = item.xpath('.//aside/span[@class="recent-author"]/a/text()').get()
            # self.logger.info(f'{index+100}- title: {replaceNT(title)}, link: {link}, imgurl: {imgurl}, tags: {tags}, recent_time: {recent_time}, recent_cat: {recent_cat}, recent_author: {recent_author}')
            # self.logger.info(f'{title}')
            data = {
                'link': link,
                'title': title,
                'content': content,
                'imgurl': imgurl,
                'tags': tags,
                'recent_time': recent_time,
                'recent_cat': recent_cat,
                'recent_author': recent_author
            }
            self.save_to_database(data)
            # yield scrapy.Request(url=link, callback=self.content_detailed)
        time.sleep(1)
        pass

    def content_detailed(self, response):
        title = response.xpath('//title/text()').get()
        text_content = response.xpath('//div[@class="single-content"]/p/text()').getall()
        # self.logger.info(f'{title}')
        # self.logger.info(f'{text_content}')
        pass

    def save_to_database(self, data):
        self.model.insert_data(data)
        pass


class MySQLDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, user, password, table_name, host='localhost', port=3306, db=None):
        if not hasattr(self, 'connect'):
            self.user = user
            self.password = password
            self.host = host
            self.port = port
            self.db = db
            self.connect = None
            self.table_name = table_name
            self.connect_database()  # 在初始化时自动执行连接操作

    def connect_database(self):
        try:
            self.connect = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                db=self.db,
                autocommit=True,
                auth_plugin_map="mysql_native_password"
            )
            self.create_table()  # 创建表
            print("Database Connected Successfully")
        except Exception as e:
            raise Exception("Database Connection Error:", e)

    def close_connection(self):
        if self.connect:
            self.connect.close()

    def insert_data(self, data: dict):
        if not self.connect:
            self.connect_database()
        try:
            db = self.connect.cursor(pymysql.cursors.DictCursor)
            title = data['title']
            imgURL = data['imgurl']
            content = data['content']
            tags = ','.join(data['tags'])
            time = ','.join(data['recent_time'])
            type = data['recent_cat']
            author = data['recent_author']
            detailsURL = data['link']

            sql = f'''
                INSERT INTO {self.table_name} (title, imgURL, content, tags, time, type, author, detailsURL)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
            db.execute(sql, (title, imgURL, content, tags, time, type, author, detailsURL))
            # print("Data Inserted Successfully")

        #             db.close()
        except Exception as e:
            # print("Error inserting data:", e)
            raise Exception("Inset Data To Database Error:", e)

    def create_table(self):

        try:
            db = self.connect.cursor(pymysql.cursors.DictCursor)
            db.execute(f"SHOW TABLES LIKE '{self.table_name}'")
            result = db.fetchone()

            if not result:  # 如果表不存在，则创建表
                sql = f'''
                CREATE TABLE `{self.table_name}` (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `title` varchar(255) DEFAULT NULL,
                  `imgURL` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
                  `content` varchar(255) DEFAULT NULL,
                  `tags` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `time` varchar(20) DEFAULT NULL,
                  `type` varchar(10) DEFAULT NULL,
                  `author` varchar(10) DEFAULT NULL,
                  `detailsURL` varchar(255) DEFAULT NULL,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=17238 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                '''
                db.execute(sql)
                self.connect.commit()
            else:
                print("Table already exists!")
        except Exception as e:
            raise Exception(f"Create MySQL Table Error: {e}")
        pass

    def search_by_title(self, title):
        try:
            db = self.connect.cursor(pymysql.cursors.DictCursor)
            sql = f"SELECT * FROM {self.table_name} WHERE title LIKE '%{title}%'"
            db.execute(sql)
            result = db.fetchall()
            return result
        except Exception as e:
            raise Exception(f"Search by Title Error: {e}")
