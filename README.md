# PyCharm_Python_AI_Data
2023年21软件1深圳职业技术大学 大作业

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
