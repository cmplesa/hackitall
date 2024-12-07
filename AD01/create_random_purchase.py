from init_products_db import products_db
from datetime import datetime
from types_of_clases import PurchasedItem, Purchase
import random

def create_random_purchase():
    item_count = random.randint(1, 20)
    if item_count < 10:
        item_count = random.randint(item_count, 10)
    elif item_count > 10:
        item_count = random.randint(10, item_count)
        
    random_days = random.randint(1, 30)
    month = 6
    purchase_date = datetime(2024, month, random_days)
    
    print(f" - Adaugam {item_count} produse in cos pentru data {purchase_date}:")
    purchase = []
    for i in range(item_count):
        product = random.choice(products_db)
        while product in purchase:
            product = random.choice(products_db)
            
        random_days = random.randint(1, 30)
        if purchase_date.day + random_days > 30:
            month += 1
            random_days = purchase_date.day + random_days - 30
        expiration_date = purchase_date.replace(day=random_days)
        
        random_discount = random.randint(10, 50)
        random_discount = random_discount - random_discount % 5 # increment to the nearest 5
        
        random_quantity = random.randint(1, 7)
        if random_quantity > 4:
            random_quantity = random.randint(1, random_quantity)
        
        if random.randint(1, 5) == 1: # 20% chance for the product to be on sale
            price = product.price - (product.price * random_discount / 100)
        else:
            price = product.price
            random_discount = 0
        print(f"  - {product.name} : {price} RON x {random_quantity} buc, expira la {expiration_date} cu {random_discount}% discount")
        purchase.append(PurchasedItem(product, purchase_date, expiration_date, price, random_quantity))
    
    return Purchase(purchase, purchase_date)