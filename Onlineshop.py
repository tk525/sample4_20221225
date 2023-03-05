import os

import Database

# 買い物カゴ
def purchase_list():

    purchaseLS = Database.purchase_pre_select()

    total_price = 0
    id_list = []
    
    for num in range(len(purchaseLS)):
        number = int(purchaseLS[num][4])
        price = int(purchaseLS[num][3])
        total_price = total_price + (number * price)

        # product_pre_id = purchaseLS[num][0]
    
    purchase_list_len = len(purchaseLS)

    return total_price, purchase_list_len

