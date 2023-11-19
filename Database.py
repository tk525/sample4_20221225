import os
import psycopg2

#カゴ
def purchase_pre_select():
    conn = psycopg2.connect(
            host="localhost",
            database="bubunhinya",
            user="admin",
            password="admin"
            # password=os.environ['DB_PASSWORD']
            )

    cur = conn.cursor()

    sql = 'SELECT * FROM test ORDER BY id ASC;'

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


#購入手続き 数量x単価 更新
def purchase_numbers_update(number_list):
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

#購入手続き 受け取り場所 名前 住所 会員情報 追加登録
def purchase_reveice_member_register(name, address, mail_address):
    conn = psycopg2.connect(
            host="localhost",
            database="bubunhinya",
            user="admin",
            password="admin"
            # password=os.environ['DB_PASSWORD']
            )
    cur = conn.cursor()

    name = "'" + name + "'"
    address = "'" + address + "'"

#     sql = "UPDATE member SET number=(%s) where id=(%s)"%(number, id_) ⭐️ログインid紐付け
    sql = "INSERT INTO member (member_name, member_address, member_mailaddress) VALUES (%s, %s, %s);"%(name, address, mail_address);

    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()

    return

#購入手続き 受け取り場所 会員情報更新 名前 住所
def purchase_reveice_member_update(member_id, name, address):
    conn = psycopg2.connect(
            host="localhost",
            database="bubunhinya",
            user="admin",
            password="admin"
            # password=os.environ['DB_PASSWORD']
            )
    cur = conn.cursor()

    name = "'" + name + "'"
    address = "'" + address + "'"

#     sql = "UPDATE member SET number=(%s) where id=(%s)"%(number, id_) ⭐️ログインid紐付け
    sql = "UPDATE member SET member_name=(%s), member_address=(%s) WHERE id=(%s) "%(name, address, member_id)

    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()

    return



#購入手続き 支払い方法 会員情報更新 クレジットカード
def purchase_payment_creditcard_member_update(creditcard, id_num):
    conn = psycopg2.connect(
            host="localhost",
            database="bubunhinya",
            user="admin",
            password="admin"
            # password=os.environ['DB_PASSWORD']
            )
    cur = conn.cursor()
    
#     sql = "UPDATE member SET number=(%s) where id=(%s)"%(number, id_) ⭐️ログインid紐付け
    sql = "UPDATE member SET member_creditcard=(%s) WHERE id=(%s) "%(creditcard, id_num)

    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()

    return



#購入手続き 支払い方法 会員情報 新規追加 クレジットカード
def purchase_payment_creditcard_member_create(creditcard, creditexpired, mailaddress):
    conn = psycopg2.connect(
            host="localhost",
            database="bubunhinya",
            user="admin",
            password="admin"
            # password=os.environ['DB_PASSWORD']
            )
    cur = conn.cursor()

#     sql = "INSERT INTO member (member_name, member_address, member_mailaddress) VALUES (%s, %s, %s);"%(name, address, mail_address);
    sql = "INSERT INTO member (member_mailaddress, member_creditcard, member_creditcard_expired_date) VALUES (%s, %s, %s);"%(mailaddress ,creditcard, creditexpired);

    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()

    return




#会員情報
def member_select(member_address):
    
    conn = psycopg2.connect(
            host="localhost",
            database="bubunhinya",
            user="admin",
            password="admin"
            # password=os.environ['DB_PASSWORD']
            )

    cur = conn.cursor()

    sql = 'SELECT * FROM member where member_mailaddress=(%s) ORDER BY id ASC;'%(member_address)

    cur.execute(sql)

    #全て取得
    show = cur.fetchall()
    print(show)

    cur.close()
    conn.close()

    return show

