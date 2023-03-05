import os
import psycopg2

def purchase_pre_select():
    conn = psycopg2.connect(
            host="localhost",
            database="bubunhinya",
            user="admin",
            password="admin"
            # password=os.environ['DB_PASSWORD']
            )

    cur = conn.cursor()

    sql = 'SELECT * FROM test;'

    cur.execute(sql)

    #全て取得
    show = cur.fetchall()

    cur.close()
    conn.close()

    return show

def purchase_pre_insert(product):
    conn = psycopg2.connect(
            host="localhost",
            database="bubunhinya",
            user="admin",
            password="admin"
            # password=os.environ['DB_PASSWORD']
            )
    cur = conn.cursor()

    product = "'" + str(product) + "'"

    sql = "INSERT INTO test (test)""VALUES (%s)"%(product)

    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()

    return 


def purchase_update(number_list):
    conn = psycopg2.connect(
            host="localhost",
            database="bubunhinya",
            user="admin",
            password="admin"
            # password=os.environ['DB_PASSWORD']
            )
    cur = conn.cursor()

    id_ = number_list[0]
    number = number_list[1]

    sql = "UPDATE test SET number=(%s) where id=(%s)"%(number, id_)

    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()

    return



