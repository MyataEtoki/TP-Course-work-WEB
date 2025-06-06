class PaymentProxy:
    """
    Прокси для управления оплатой с разных источников баланса.

    :param get_balance_func: функция получения текущего баланса
    :param set_balance_func: функция установки нового баланса
    :param name: название источника (наличные, карта, бонусы)
    """

    def __init__(self, get_balance_func, set_balance_func, name):
        self._get = get_balance_func
        self._set = set_balance_func
        self.name = name

    def pay(self, amount):
        """
        Попытка списания указанной суммы с баланса.

        :param amount: сумма для списания
        :return: кортеж (успех: bool, сообщение: str)
        """
        balance = self._get()
        if balance >= amount:
            self._set(balance - amount)
            return True, f"Оплачено {self.name} на сумму {amount}₽"
        return False, f"Недостаточно средств на {self.name} (требуется {amount}₽, есть {balance}₽)"
