class Product:
    def __init__(self, name, price, requires_weight=False):
        self.name = name
        self.base_price = price
        self.requires_weight = requires_weight
        self.weight = None

    def set_weight(self, weight):
        self.weight = float(weight)

    @property
    def price(self):
        return self.base_price * self.weight if self.requires_weight and self.weight else self.base_price

    def is_ready(self):
        return not self.requires_weight or self.weight is not None


class Customer:
    def __init__(self):
        self.cash = 100
        self.card = 100
        self.bonus = 50
        self.cart = []
        self.purchase_history = []

    def total_cart(self):
        return sum(item.price for item in self.cart)

    def pay(self, amount, cash, card, bonus):
        if cash + card + bonus != amount:
            return False, "Сумма не совпадает с общей стоимостью"
        if cash > self.cash or card > self.card or bonus > self.bonus:
            return False, "Недостаточно средств"
        self.cash -= cash
        self.card -= card
        self.bonus -= bonus

        # сохраняем историю
        items = [(p.name, p.price) for p in self.cart]
        self.purchase_history.append({
            "items": items,
            "total": amount,
            "method": {"cash": cash, "card": card, "bonus": bonus}
        })

        self.cart = []
        return True, "Оплата прошла успешно"

    def go_to_work(self):
        self.cash += 500
        self.card += 300
        self.bonus += 200
        return True, "Вы заработали: +500₽ нал, +300₽ карта, +200₽ бонусы. И диарею."
