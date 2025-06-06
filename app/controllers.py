from .models import Product, Customer
from .payment_proxy import PaymentProxy # паттерн Прокси
import json

def load_products_from_json(filepath='products.json'):
    with open(filepath, encoding='utf-8') as f:
        data = json.load(f)
    products = []
    for p in data:
        products.append(Product(p['id'], p['name'], p['price'], p.get('requires_weight', False)))
    return products


class Controller:
    def __init__(self):
        self.products = load_products_from_json(filepath='products.json')
        self.customer = Customer()
        self.proxies = [
            PaymentProxy(lambda: self.customer.cash, lambda v: setattr(self.customer, 'cash', v), "наличных"),
            PaymentProxy(lambda: self.customer.card, lambda v: setattr(self.customer, 'card', v), "карте"),
            PaymentProxy(lambda: self.customer.bonus, lambda v: setattr(self.customer, 'bonus', v), "бонусах")
        ]

    def get_products(self):
        return self.products

    def get_cart(self):
        return self.customer.cart

    def add_to_cart(self, index, weight=None):
        try:
            product = self.products[int(index)]
            if product.requires_weight:
                if not weight:
                    return False, "Этот товар нужно взвесить"
                product = Product(product.id, product.name, product.base_price, True)
                product.set_weight(weight)
            self.customer.cart.append(product)
            return True, f"{product.name} добавлен(а) в корзину"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"

    def pay_with_proxies(self, amounts):
        total = self.customer.total_cart()
        paid = 0
        messages = []

        for proxy, amount in zip(self.proxies, amounts):
            amount = float(amount or 0)
            success, msg = proxy.pay(amount)
            messages.append(msg)
            if success:
                paid += amount

        if paid >= total:
            items = [(p.name, p.price) for p in self.customer.cart]
            self.customer.purchase_history.append({
                "items": items,
                "total": total,
                "method": {"cash": amounts[0], "card": amounts[1], "bonus": amounts[2]}
            })
            self.customer.cart = []
            return True, "Покупка совершена. " + "; ".join(messages)
        else:
            return False, "Недостаточно средств. " + "; ".join(messages)

    def go_to_work(self):
        self.customer.cash += 500
        self.customer.card += 300
        self.customer.bonus += 200
        return True, "Вы заработали: +500₽ нал, +300₽ карта, +200₽ бонусы. И невроз."
