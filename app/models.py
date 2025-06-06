class Product:
    """
    Класс товара. Поддерживает обычные и весовые товары.
    """

    def __init__(self, id, name, price, requires_weight=False):
        """
        Инициализация товара.
        :param id: идентификатор
        :param name: название товара
        :param price: базовая цена за штуку или за 1 кг
        :param requires_weight: требуется ли взвешивание
        """
        self.id = id
        self.name = name
        self.base_price = price
        self.requires_weight = requires_weight
        self.weight = None

    def set_weight(self, weight):
        """Установка веса товара (если требуется)"""
        self.weight = float(weight)

    @property
    def price(self):
        """Расчёт итоговой цены с учётом веса, если нужно"""
        return self.base_price * self.weight if self.requires_weight and self.weight else self.base_price

    def is_ready(self):
        """Проверка, готов ли товар к покупке (взвешен ли он, если требуется)"""
        return not self.requires_weight or self.weight is not None


class Customer:
    """
    Класс покупателя. Хранит баланс по разным способам оплаты,
    корзину и историю покупок.
    """

    def __init__(self):
        """Инициализация покупателя с начальными балансами"""
        self.cash = 100
        self.card = 100
        self.bonus = 50
        self.cart = []
        self.purchase_history = []

    def total_cart(self):
        """Подсчёт общей стоимости товаров в корзине"""
        return sum(item.price for item in self.cart)

    def pay(self, amount, cash, card, bonus):
        """
        Оплата товаров.
        Проверяет сумму и доступность средств,
        списывает средства и сохраняет историю.
        """
        if cash + card + bonus != amount:
            return False, "Недостаточно средств, Сумма не совпадает с общей стоимостью"
        if cash > self.cash or card > self.card or bonus > self.bonus:
            return False, "Недостаточно средств"

        self.cash -= cash
        self.card -= card
        self.bonus -= bonus

        self.purchase_history.append({
            "items": [(p.name, p.price) for p in self.cart],
            "total": amount,
            "method": {"cash": cash, "card": card, "bonus": bonus}
        })

        self.cart = []
        return True, "Оплата прошла успешно"

    def go_to_work(self):
        """
        Пополнение баланса покупателя (симуляция работы)
        """
        self.cash += 500
        self.card += 300
        self.bonus += 200
        return True, "Вы заработали: +500₽ нал, +300₽ карта, +200₽ бонусы. И диарею."
