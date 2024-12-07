from init_products_db import products_db
from types_of_clases import PurchasedItem, Purchase
import random

def generate_random_promotions():
    promotional_products = []
    total_products = len(products_db)
    promotions_count = random.randint(1, (int)(total_products / 3))
    print(f"\nSe vor adauga {promotions_count} produse in promotie.")
    for i in range(promotions_count):
        product = random.choice(products_db)
        while product in promotional_products:
            product = random.choice(products_db)
        promotional_products.append(product)
        print(f"Produsul {product.name} cu id-ul {product.product_id} a fost adaugat in promotie.")
    return promotional_products