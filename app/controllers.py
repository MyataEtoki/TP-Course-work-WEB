from .models import Product, Customer
from .payment_proxy import PaymentProxy  # Используем паттерн Прокси для оплаты
import json

def load_products_from_json(filepath='products.json'):
    """
    Загружает список товаров из JSON-файла.

    :param filepath: путь к JSON-файлу с товарами
    :return: список объектов Product
    """
    with open(filepath, encoding='utf-8') as f:
        data = json.load(f)
    products = []
    for p in data:
        products.append(Product(p['id'], p['name'], p['price'], p.get('requires_weight', False)))
    return products


class Controller:
    """
    Контроллер бизнес-логики приложения.

    Отвечает за работу с товарами, корзиной и оплатой через прокси-объекты.
    """

    def __init__(self):
        """
        Инициализация контроллера:
        - загружает товары из JSON,
        - создает объект покупателя,
        - создает прокси для разных способов оплаты.
        """
        self.products = load_products_from_json(filepath='products.json')
        self.customer = Customer()
        self.proxies = [
            PaymentProxy(lambda: self.customer.cash, lambda v: setattr(self.customer, 'cash', v), "наличных"),
            PaymentProxy(lambda: self.customer.card, lambda v: setattr(self.customer, 'card', v), "карте"),
            PaymentProxy(lambda: self.customer.bonus, lambda v: setattr(self.customer, 'bonus', v), "бонусах")
        ]

    def get_products(self):
        """
        Получить список всех доступных товаров.

        :return: список объектов Product
        """
        return self.products

    def get_cart(self):
        """
        Получить текущие товары в корзине покупателя.

        :return: список объектов Product
        """
        return self.customer.cart

    def add_to_cart(self, index, weight=None):
        """
        Добавить товар в корзину.

        Если товар требует веса, обязательно нужно указать параметр weight.

        :param index: индекс товара в списке товаров
        :param weight: вес товара (если требуется)
        :return: кортеж (успех: bool, сообщение: str)
        """
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
        """
        Оплатить товары из корзины с использованием нескольких способов оплаты.

        :param amounts: список сумм для списания [наличные, карта, бонусы]
        :return: кортеж (успех: bool, сообщение: str)
        """
        total = self.customer.total_cart()
        total_payment = sum(float(a or 0) for a in amounts)

        if total_payment < total:
            return False, f"Недостаточно средств для оплаты. Нужно {total}₽, а вы указали {total_payment}₽."

        paid = 0
        messages = []
        change = total_payment - total
        remaining = total

        for proxy, amount in zip(self.proxies, amounts):
            amount = float(amount or 0)
            to_pay = min(amount, remaining)
            success, msg = proxy.pay(to_pay)
            messages.append(msg)
            if success:
                paid += to_pay
                remaining -= to_pay
            else:
                return False, "Ты шо обманываешь. Нет у тебя денег. Плоти штраф."

        # Сохраняем историю покупок и очищаем корзину
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

        change_msg = f" Ваша сдача: {change:.2f}₽." if change > 0 else ""
        return True, "Покупка совершена." + change_msg + " " + "; ".join(messages)

    def go_to_work(self):
        """
        Игровая механика: пополнение баланса покупателя.

        Увеличивает наличные, баланс карты и бонусы.

        :return: кортеж (успех: bool, сообщение: str)
        """
        self.customer.cash += 500
        self.customer.card += 300
        self.customer.bonus += 200
        return True, "Вы заработали: +500₽ нал, +300₽ карта, +200₽ бонусы. И невроз."
