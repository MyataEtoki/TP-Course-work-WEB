from abc import ABC, abstractmethod

class Command(ABC):
    """Абстрактный класс команды с методом execute."""

    @abstractmethod
    def execute(self):
        """Выполнить команду."""
        pass


class AddToCartCommand(Command):
    """Команда для добавления товара в корзину."""

    def __init__(self, controller, product_index, weight=None):
        """
        :param controller: контроллер приложения
        :param product_index: индекс товара в списке
        :param weight: вес товара (если требуется)
        """
        self.controller = controller
        self.product_index = product_index
        self.weight = weight

    def execute(self):
        """Выполнить добавление товара в корзину."""
        return self.controller.add_to_cart(self.product_index, self.weight)


class PayCommand(Command):
    """Команда для оплаты товаров."""

    def __init__(self, controller, amounts):
        """
        :param controller: контроллер приложения
        :param amounts: список сумм для оплаты [наличные, карта, бонусы]
        """
        self.controller = controller
        self.amounts = amounts

    def execute(self):
        """Выполнить оплату с проверкой формата сумм."""
        try:
            cash = float(self.amounts[0])
            card = float(self.amounts[1])
            bonus = float(self.amounts[2])
        except (ValueError, TypeError, IndexError):
            return False, "Неверный формат введённых сумм."

        return self.controller.pay_with_proxies([cash, card, bonus])


class WorkCommand(Command):
    """Команда для пополнения баланса (симуляция работы)."""

    def __init__(self, controller):
        """
        :param controller: контроллер приложения
        """
        self.controller = controller

    def execute(self):
        """Выполнить пополнение баланса."""
        return self.controller.go_to_work()
