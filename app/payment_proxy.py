class PaymentProxy:
    def __init__(self, get_balance_func, set_balance_func, name):
        self._get = get_balance_func
        self._set = set_balance_func
        self.name = name

    def pay(self, amount):
        balance = self._get()
        if balance >= amount:
            self._set(balance - amount)
            return True, f"Оплачено {self.name} на сумму {amount}₽"
        return False, f"Недостаточно средств на {self.name} (требуется {amount}₽, есть {balance}₽)"
