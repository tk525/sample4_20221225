import os
import json 
import re
import datetime, calendar
from flask import Flask, render_template, request, redirect, url_for, jsonify

import Database, Onlineshop

# app = Flask(__name__)
app = Flask(__name__, static_folder='./templates/') 


# オンラインショップ
@app.route('/')
def onlineshop():

    total_price = Onlineshop.purchase_list()[0]
    purchaseLS_len = Onlineshop.purchase_list()[1]
    dates_purchaseLS = Database.purchase_pre_select()
    # product_id = Onlineshop.purchase_list()[2] いらんかも

    return render_template('index.html', purchase_list=dates_purchaseLS, total_price=total_price, purchaseLS_len=purchaseLS_len)

@app.route('/onlineshop_post', methods=['POST'])
def onlineshop_post():

    # データベース挿入
    product = request.form['for_post']
    Database.purchase_pre_insert(product)

    # データベース データ取得
    dates_purchaseLS = Database.purchase_pre_select()
    total_price = Onlineshop.purchase_list()[0]
    purchaseLS_len = Onlineshop.purchase_list()[1]

    return render_template('index.html', purchase_list=dates_purchaseLS, total_price=total_price, purchaseLS_len=purchaseLS_len)





# 購入手続き
@app.route("/purchase")
def purchase():

    # データベース かご データ取得
    total_price = Onlineshop.purchase_list()[0]
    purchaseLS_len = Onlineshop.purchase_list()[1]
    dates_purchaseLS = Database.purchase_pre_select()

    # データベース 会員情報 データ取得
    member_address = "'handsome@gmail.com'"
    member_info_pre = Database.member_select(member_address)

    # member_nameがNoneじゃない値だけ収集
    member_info = []
    for num in range(len(member_info_pre)):    
        if member_info_pre[num][1] != None:
            member_info.append(member_info_pre[num])

    member_id=[]
    member_name=[]
    member_address=[]
    member_creditcard=[]
    member_infoLS_len=len(member_info)
    for i in range(len(member_info)):
        member_id.append(member_info[i][0])
        member_name.append(member_info[i][1])
        member_address.append(member_info[i][2])
        member_creditcard.append(str(member_info[i][4]))
    
    # 配送日未指定
    def get_last_date(dt):
        return dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])
    today = datetime.datetime.today()
    fivedays_later = today.day + 5
    fivedays_later = 31 #テスト用
    last_day = int(get_last_date(today).strftime('%d'))

    if last_day < fivedays_later:
        day = str(fivedays_later - last_day)
        month = str(today.month + 1)
    elif last_day >= fivedays_later:
        day = str(fivedays_later)
        month = str(today.month)
    auto_delivery_date = month + "月" + day + "日"

    



    return render_template('purchase.html',
                           purchase_list=dates_purchaseLS, total_price=total_price, purchaseLS_len=purchaseLS_len, auto_delivery_date=auto_delivery_date,
                            member_infoLS_len=member_infoLS_len, member_id=member_id ,member_name=member_name,
                           member_address=member_address, member_creditcard=member_creditcard,
                           )

#購入手続き/モーダル 数量x単価 再計算
@app.route('/onlineshop_ajax', methods=['POST'])
def onlineshop_ajax():

    if request.method == "POST":


        purchase_number_list = request.form["data"]
        id_with_number = purchase_number_list.split(",")

        #数量更新
        Database.purchase_numbers_update(id_with_number)
        
        #単価の値取得
        total_price = Onlineshop.purchase_list()[0]
        purchaseLS_len = Onlineshop.purchase_list()[1]

        dict = {"total_price": total_price}

    return json.dumps(dict)

#購入手続き 受け取り場所
@app.route('/onlineshop_receive_ajax', methods=['POST'])
def onlineshop_receive_ajax():

    if request.method == "POST":


        member_id = request.form["member_id"]
        name = request.form["name"]
        address = request.form["address"]

        if member_id == '0':
            #名前、住所 追加登録
            member_address = "'handsome@gmail.com'"
            Database.purchase_reveice_member_register(name, address, member_address)
        elif member_id != '0':
            #名前、住所 更新
            Database.purchase_reveice_member_update(member_id, name, address)
        
        # データベース 会員情報 データ取得
        member_address = "'handsome@gmail.com'"
        member_info = Database.member_select(member_address)
        member_infoLS_len = len(member_info)

        member_id=[]
        member_name=[]
        member_address=[]
        member_creditcard=[]
        for i in range(len(member_info)):
            member_id.append(member_info[i][0])
            member_name.append(member_info[i][1])
            member_address.append(member_info[i][2])
            member_creditcard.append(str(member_info[i][4]))

        dict = {"member_infoLS_len":member_infoLS_len ,"member_id": member_id, "member_name": member_name,
                "member_address": member_address ,"member_creditcard": member_creditcard}

    return json.dumps(dict)



#購入手続き 受け取り場所
@app.route('/onlineshop_receive_delete', methods=['POST'])
def onlineshop_receive_delete():

    if request.method == "POST":
       member_id = request.form["member_id"]
       print("はは")
    return render_template('index.html')


#購入手続き 支払い方法 クレジットカード
@app.route('/onlineshop_receive_ajax_credit', methods=['POST'])
def onlineshop_receive_ajax_credit():

    if request.method == "POST":


        id_num = request.form["num"]
        creditcard = request.form["creditcard"]
        creditexpired = request.form["creditexpired"]

        id_num = int(id_num) + 1;

        # 既存のクレカ情報更新
        if creditexpired == "0" and creditcard != "": #フォーム開いて閉じただけの場合の処理
            Database.purchase_payment_creditcard_member_update(creditcard, id_num);

        # 新規クレカ登録
        elif creditexpired != "0" and creditcard != "":
            member_address = "'handsome@gmail.com'"
            Database.purchase_payment_creditcard_member_create(creditcard, creditexpired, member_address);

        # データベース 会員情報 データ取得
        member_address = "'handsome@gmail.com'"
        member_info = Database.member_select(member_address)
        member_infoLS_len = len(member_info)

        member_creditcard=[]
        for i in range(len(member_info)):
            member_creditcard.append(str(member_info[i][4]))

        dict = {"member_creditcard": member_creditcard}

    return json.dumps(dict)



# 購入手続き 完了
@app.route("/purchase_done")
def purchase_done():
    


    return render_template('purchase_done.html',)

if __name__ == "__main__":
    app.run(debug=True)
