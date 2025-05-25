from app.models import Product, Customer

class StoreController:
    def __init__(self):
        self.products = [
            Product("Яблоки", 100, requires_weight=True),
            Product("Хлеб", 40),
            Product("Массаж", 1500)
        ]
        self.customer = Customer()

    def get_products(self):
        return self.products

    def get_cart(self):
        return self.customer.cart

    def add_to_cart(self, index, weight=None):
        product = self.products[index]
        if product.requires_weight:
            if weight:
                product.set_weight(weight)
            else:
                return False, "Не указан вес"
        if product.is_ready():
            self.customer.cart.append(product)
            return True, "Товар добавлен"
        return False, "Товар не готов к добавлению"

    def remove_from_cart(self, index):
        if 0 <= index < len(self.customer.cart):
            self.customer.cart.pop(index)

    def attempt_purchase(self, cash, card, bonus):
        total = self.customer.total_cart()
        return self.customer.pay(total, cash, card, bonus)
