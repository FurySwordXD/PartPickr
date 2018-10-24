import pymysql

conn = pymysql.connect(host='localhost', user='root', password='', db='partpickr')
cursor = conn.cursor()

sql = """INSERT INTO users(Email, Password, Name, Age) VALUES ("xxxqwe","eqw", "sdfwe", 21)"""
cursor.execute(sql)
conn.commit()
