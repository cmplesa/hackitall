from datetime import datetime
from collections import Counter
import statistics
from save_category_tags import CATEGORY_TAGS

class Product:
    def __init__(self, product_id, name, category, price, weight):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.weight = weight
        self.tags = CATEGORY_TAGS.get(self.category, [])

    def set_price_category(self, prices):
        price_category = ""
        if self.price < prices["first_third_price"]:
            price_category = "ieftin"
        elif prices["first_third_price"] <= self.price < prices["second_third_price"]:
            price_category = "mediu"
        else:
            price_category = "scump"
        self.price_category = price_category


class PurchasedItem:
    def __init__(self, product: Product, purchase_date: datetime, expiration_date: datetime, purchased_price: float, quantity=1):
        self.product = product
        self.purchase_date = purchase_date
        self.expiration_date = expiration_date
        self.purchased_price = purchased_price
        self.quantity = quantity
        self.discount_percentage = self.calculate_discount()

    def calculate_discount(self):
        if self.product.price == 0:
            return 0.0
        discount = ((self.product.price - self.purchased_price) / self.product.price) * 100
        return round(discount, 2)


class Purchase:
    def __init__(self, purchased_items, purchase_date):
        self.purchased_items = purchased_items
        self.purchase_date = purchase_date
        self.total_price = self.calculate_total_price()

    def calculate_total_price(self):
        return sum(item.purchased_price * item.quantity for item in self.purchased_items)


class User:
    def __init__(self, user_id, birth_year, purchases=None, other_info=None):
        self.user_id = user_id
        self.birth_year = birth_year
        self.purchases = purchases if purchases else []  # list of Purchase
        self.other_info = other_info if other_info else {}

    def add_purchase(self, purchase: Purchase):
        self.purchases.append(purchase)

    def compute_profile(self):
        profile = {}

        if not self.purchases:
            profile["preferred_categories"] = []
            profile["price_preference"] = "N/A"
            profile["family_size_estimate"] = "N/A"
            profile["purchase_frequency"] = 0
            profile["most_purchased_products"] = []
            profile["lifestyle"] = []
            return profile

        all_items = []
        all_dates = []
        total_price = 0
        for p in self.purchases:
            all_items.extend(p.purchased_items)
            all_dates.append(p.purchase_date)
            total_price += p.total_price

        if not all_items:
            profile["preferred_categories"] = []
            profile["price_preference"] = "N/A"
            profile["family_size_estimate"] = "N/A"
            profile["purchase_frequency"] = "Nu exista destule date"
            profile["most_purchased_products"] = []
            profile["lifestyle"] = []
            return profile

        categories = [item.product.category for item in all_items for _ in range(item.quantity)]
        top_categories = [cat for cat, count in Counter(categories).most_common()]
        
        price_cats = [item.product.price_category for item in all_items for _ in range(item.quantity)]
        most_common_price_cat = [cat for cat, count in Counter(price_cats).most_common()]

        dates = sorted(all_dates)
        if len(dates) > 1:
            diffs = [(dates[i+1]-dates[i]).days for i in range(len(dates)-1)]
            if diffs:
                avg_days_between_purchases = statistics.mean(diffs)
                purchase_frequency = round(30/avg_days_between_purchases,1)
            else:
                purchase_frequency = -1
        else:
            purchase_frequency = -1

        total_quantity = sum(item.quantity for item in all_items)
        average_quantity = total_quantity / len(self.purchases)
        family_size = round((average_quantity - 20) / 15 + 1)

        product_names = [item.product.name for item in all_items for _ in range(item.quantity)]
        top_products = [prod for prod, count in Counter(product_names).most_common()]

        all_tags = []
        for it in all_items:
            all_tags.extend(it.product.tags * it.quantity)
        tag_counter = Counter(all_tags)
        print(f"Tag counter: {tag_counter}")
        # saves in lifestyle_tags, in order of most common tags, the tags of which the count is >= mean of all tags
        mean_tag_count = statistics.mean(tag_counter.values())
        lifestyle_tags = [tag for tag, count in tag_counter.items() if count >= mean_tag_count]
        

        profile["preferred_categories"] = top_categories
        profile["price_preference"] = most_common_price_cat
        profile["family_size_estimate"] = family_size
        profile["purchase_frequency"] = purchase_frequency
        profile["most_purchased_products"] = top_products
        profile["lifestyle"] = lifestyle_tags
        self.profile = profile


class RecommendationEngine:
    def __init__(self, promotional_products):
        self.promotional_products = promotional_products  # list of Product

    def recommend(self, user: User):
        profile = user.profile

        recommended = []
        reasons = {}

        preferred_categories = profile.get("preferred_categories", [])
        preferred_price_cat = profile.get("price_preference", "")
        lifestyle = profile.get("lifestyle", [])

        for p in self.promotional_products:
            reason_list = []

            # daca produsul e in una din categoriile preferate
            if p.category in preferred_categories:
                reason_list.append("Apartine unei categorii preferate")

            # daca produsul se incadreaza in categoria de pret preferata
            if p.price_category == preferred_price_cat:
                reason_list.append("Se incadreaza in categoria de pret preferata")

            # In functie de lifestyle:
            # daca "sanatos"
            if "sanatos" in lifestyle and "healthy" in p.tags:
                reason_list.append("Potrivit pentru un stil de viata sanatos")

            # daca consuma multe dulciuri
            if "consum multe dulciuri" in lifestyle and "sweets" in p.tags:
                reason_list.append("Se potriveste cu preferinta pentru dulciuri")

            # daca merge la sala
            if "merge la sala" in lifestyle and "gym" in p.tags:
                reason_list.append("Potrivit pentru stil de viata activ")

            # daca este vegan
            if "vegan" in lifestyle and "vegan" in p.tags:
                reason_list.append("Potrivit pentru dieta vegana")

            # daca prefera ready-to-eat
            if "prefer ready-to-eat" in lifestyle and "ready_to_eat" in p.tags:
                reason_list.append("Potrivit pentru preferinta de ready-to-eat")

            # Popular (ex: pret peste 10)
            if p.price > 10:
                reason_list.append("Produs popular (multi il cumpara)")

            if reason_list:
                recommended.append(p)
                reasons[p.product_id] = reason_list

        recommended.sort(key=lambda prod: len(reasons[prod.product_id]), reverse=True)

        return recommended, reasons