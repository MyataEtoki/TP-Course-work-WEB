from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class AddToCartCommand(Command):
    def __init__(self, controller, product_index, weight=None):
        self.controller = controller
        self.product_index = product_index
        self.weight = weight

    def execute(self):
        return self.controller.add_to_cart(self.product_index, self.weight)


class PayCommand(Command):
    def __init__(self, controller, amounts):
        """
        :param controller: контроллер приложения
        :param amounts: список строк/чисел, соответствующих [наличные, карта, бонусы]
        """
        self.controller = controller
        self.amounts = amounts

    def execute(self):
        return self.controller.pay_with_proxies(self.amounts)


class WorkCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        return self.controller.go_to_work()
