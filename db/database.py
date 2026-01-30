import pymysql

def get_db():
    connection = pymysql.connect(
        host='mysql-gmessal.alwaysdata.net',
        user='gmessal',
        password='aR%j=fO/5;#~0qau*8CX',
        database='gmessal_hub',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
