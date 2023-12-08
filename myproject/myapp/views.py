from django.shortcuts import render
import pymysql

def my_view(request):
    sql = MySQLDatabase2(user='root', password='root', table_name='PageForImage', db='photoworldForPython')
    if request.method == 'POST':
        search_query = request.POST.get('search_query')  # 获取输入框的内容
        result = sql.search_by_title(title=search_query)
        result_length = len(result)
        return render(request, 'my_template.html', {'result': result, 'result_length': result_length})
    return render(request, 'my_template.html', {'result': [], 'result_length': 0})


def search_by_bags(request):
    sql = MySQLDatabase2(user='root', password='root', table_name='PageForImage', db='photoworldForPython')
    if request.method == 'POST':
        search_query = request.POST.get('search_query_for_tags')  # 获取输入框的内容
        result = sql.search_by_bag(title=search_query)
        result_length = len(result)
        return render(request, 'my_template.html', {'result': result, 'result_length': result_length})
    return render(request, 'my_template.html', {'result': [], 'result_length': 0})

def search_by_author(request):
    sql = MySQLDatabase2(user='root', password='root', table_name='PageForImage', db='photoworldForPython')
    if request.method == 'POST':
        search_query = request.POST.get('search_query_for_author')  # 获取输入框的内容
        result = sql.search_by_author(title=search_query)
        result_length = len(result)
        return render(request, 'my_template.html', {'result': result, 'result_length': result_length})
    return render(request, 'my_template.html', {'result': [], 'result_length': 0})





class MySQLDatabase2:
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

    def search_by_bag(self, tag):
        try:
            db = self.connect.cursor(pymysql.cursors.DictCursor)
            sql = f"SELECT * FROM {self.table_name} WHERE tags LIKE '%{tag}%'"
            db.execute(sql)
            result = db.fetchall()
            return result
        except Exception as e:
            raise Exception(f"Search by Tag Error: {e}")