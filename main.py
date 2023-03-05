import os
import json 
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify

import Database, Onlineshop

# app = Flask(__name__)
app = Flask(__name__, static_folder='./templates/') 


# オンラインショップ
@app.route('/')
def onlineshop():

    dates_purchaseLS = Database.purchase_pre_select()
    total_price = Onlineshop.purchase_list()[0]
    purchaseLS_len = Onlineshop.purchase_list()[1]
    # product_id = Onlineshop.purchase_list()[2] いらんかも

    return render_template('index.html', purchase_list=dates_purchaseLS, total_price=total_price, 
                           purchaseLS_len=purchaseLS_len, 
                        #    product_id=product_id
                           )

@app.route('/onlineshop_post', methods=['POST'])
def onlineshop_post():

    # データベース挿入
    product = request.form['for_post']
    Database.purchase_pre_insert(product)

    # データベース データ取得
    purchase_list = Database.purchase_pre_select()

    return render_template('index.html', purchase_list=purchase_list)



@app.route('/onlineshop_ajax', methods=['POST'])
def onlineshop_ajax():

    if request.method == "POST":


        purchase_number_list = request.form["data"]
        id_with_number = purchase_number_list.split(",")

        #数量更新
        Database.purchase_update(id_with_number)
        
        #単価の値取得
        total_price = Onlineshop.purchase_list()[0]
        purchaseLS_len = Onlineshop.purchase_list()[1]

        dict = {"total_price": total_price}

    return json.dumps(dict)



# 購入手続き
@app.route("/purchase")
def purchase():

    fuck="hey"

    return render_template('purchase.html', fuck=fuck)

if __name__ == "__main__":
    app.run(debug=True)
