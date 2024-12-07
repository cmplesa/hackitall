from datetime import datetime

from init_products_db import products_db
from create_random_purchase import create_random_purchase
from types_of_clases import Product, PurchasedItem, Purchase, User, RecommendationEngine
from create_random_promotions import generate_random_promotions

def calculate_mean_price():
    mean_price = sum(p.price for p in products_db) / len(products_db)
    min_price = min(p.price for p in products_db)
    max_price = max(p.price for p in products_db)
    
    first_third_price = (mean_price + min_price) / 2
    second_third_price = (mean_price + max_price) / 2
    prices = { "min_price": min_price, "first_third_price": first_third_price, "second_third_price": second_third_price, "max_price": max_price }
    
    return prices

def update_price_categories(prices):
    for p in products_db:
        p.set_price_category(prices)

if __name__ == "__main__":
    prices = calculate_mean_price()
    update_price_categories(prices) # setam categoriile de pret pentru produse
    
    now = datetime.now()
    user = User(user_id=1001, birth_year=1985)
    
    for i in range(5):
        print(f"Achizita {i+1} pentru utilizatorul {user.user_id}:")
        purchase = create_random_purchase()
        user.add_purchase(purchase)
        
    user.compute_profile()
    print("\nProfil utilizator:", user.profile)

    promotional_products = generate_random_promotions()
    engine = RecommendationEngine(promotional_products)
    recommended_products, reasons = engine.recommend(user)

    print("\nRecomandari:")
    for p in recommended_products:
        print(f"Produs: {p.name} | Motive: {', '.join(reasons[p.product_id])}")
