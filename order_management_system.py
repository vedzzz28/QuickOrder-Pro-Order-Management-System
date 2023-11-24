import csv
import random
from collections import defaultdict

class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.popularity = 0

class Order:
    def __init__(self, order_id, customer_name, products):
        self.order_id = order_id
        self.customer_name = customer_name
        self.products = products
        self.status = "Placed"
        self.calculate_total_price()

    def calculate_total_price(self):
        self.total_price = sum(product.price for product in self.products)

    def set_status(self, status):
        self.status = status

class OrderManagementSystem:
    def __init__(self):
        self.products = self.load_products_from_csv("products.csv")
        self.products_dict = defaultdict(list)
        self.orders = []

        for product in self.products:
            self.products_dict[product.product_id].append(product)

    def load_products_from_csv(self, filename):
        products = []
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                product = Product(int(row[0]), row[1], float(row[2]))
                products.append(product)
        return products

    def place_order(self, customer_name, product_ids):
        order_id = len(self.orders) + 1
        products = [product for product_id in product_ids for product in self.products_dict[product_id]]
        for product in products:
            product.popularity += 1
        order = Order(order_id, customer_name, products)
        self.orders.append(order)
        return order

    def fulfill_orders(self):
        for order in self.orders:
            order.status = "Fulfilled"

    def track_order(self, order_id):
        order = next((order for order in self.orders if order.order_id == order_id), None)
        return order.status if order else "Order not found"

    def recommend_products(self, customer_name):
        # Greedy algorithm: Recommend the most popular product
        products_by_popularity = sorted(self.products, key=lambda x: x.popularity, reverse=True)
        for product in products_by_popularity:
            if random.choice([True, False,False,False]):  # Add some randomness to the recommendation
                return product
        return None

    def get_order_by_id(self, order_id):
        for order in self.orders:
            if order.order_id == order_id: 
                return order
        return None

    def get_order(self, order_id):
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None