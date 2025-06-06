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
        # Проверим сначала сумму, которую хочет оплатить пользователь
        total_payment = sum(float(a or 0) for a in amounts)

        if total_payment < total:
            return False, f"Недостаточно средств для оплаты. Нужно {total}₽, а вы указали {total_payment}₽."

        paid = 0
        messages = []
        change = total_payment - total  # сдача

        # Чтобы списывать ровно сумму total, а не больше, распределим оплату по проксям
        remaining = total
        for proxy, amount in zip(self.proxies, amounts):
            amount = float(amount or 0)
            # Списываем либо всю сумму amount, либо только то, что осталось оплатить
            to_pay = min(amount, remaining)
            success, msg = proxy.pay(to_pay)
            messages.append(msg)
            if success:
                paid += to_pay
                remaining -= to_pay

        # Оплата завершена, оформим историю и очистим корзину
        items = [(p.name, p.price) for p in self.customer.cart]
        self.customer.purchase_history.append({
            "items": items,
            "total": total,
            "method": {
                "cash": min(float(amounts[0] or 0), total),
                "card": min(float(amounts[1] or 0), max(0, total - float(amounts[0] or 0))),
                "bonus": min(float(amounts[2] or 0), max(0, total - float(amounts[0] or 0) - float(amounts[1] or 0)))
            }
        })
        self.customer.cart = []

        # Формируем сообщение о сдаче, если она есть
        change_msg = f" Ваша сдача: {change:.2f}₽." if change > 0 else ""
        return True, "Покупка совершена." + change_msg + " " + "; ".join(messages)

    def go_to_work(self):
        self.customer.cash += 500
        self.customer.card += 300
        self.customer.bonus += 200
        return True, "Вы заработали: +500₽ нал, +300₽ карта, +200₽ бонусы. И невроз."
