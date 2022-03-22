import pymysql
from movie_spider import url,getData

dic = getData(url)

db = pymysql.connect(host="localhost",user="root",password="123456",database="db_movies")

# sql_creatdb = "CREATE DATABASE IF NOT EXISTS db_movies"
cursor = db.cursor()
# cursor.execute(sql_creatdb)

sql_drop = '''
    drop table if exists movies;
'''
cursor.execute(sql_drop)

sql_creattable = '''
        CREATE TABLE IF NOT EXISTS movies
            (m_name char(40) primary key,
            score float,
            score_people int,
            quote text,
            director char(40),
            actor char(40),
            m_type char(40),
            contr char(40),
            m_year char(40) 
            )ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
cursor.execute(sql_creattable)

for value in dic.values():
    tuple_value = tuple(value)
    cursor.execute('insert into movies values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',tuple_value)
db.commit()
db.close()