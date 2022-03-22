import sqlite3
from movie_spider import getData,url

dic = getData(url)

conn = sqlite3.connect("./test.db")
c = conn.cursor()

sql = '''
        CREATE TABLE IF NOT EXISTS movies
            (m_name text primary key,
            score real,
            score_people integer,
            quote text,
            director varchar,
            actor varchar,
            m_type varchar,
            contr varchar,
            m_year varchar    
            )
        '''
c.execute(sql)

for value in dic.values():
    # sql1 = '''
    #     insert into movies values("%s","%s","%s","%s","%s","%s","%s","%s","%s")
    # '''%(value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8])
    
    tuple_value = tuple(value)
    c.execute('insert into movies values(?,?,?,?,?,?,?,?,?)',tuple_value)
conn.commit()
conn.close()
print("成功打开数据库")

# for value in dic.values():
#     print(value[0])