import pymysql
import pymysql.cursors

def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="aura_spa",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )