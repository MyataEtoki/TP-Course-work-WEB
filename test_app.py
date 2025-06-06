import unittest
from app.models import Product, Customer
from app.controllers import Controller

# запуск - в терминал: python -m unittest test_app.py

class TestCustomer(unittest.TestCase):
    """Тесты для класса Customer: проверка оплаты и работы с корзиной"""

    def test_successful_payment(self):
        """Проверка успешной оплаты при точном соответствии суммы"""
        customer = Customer()
        customer.cart = [Product(0, "Хлеб", 50)]
        success, msg = customer.pay(50, 50, 0, 0)
        self.assertTrue(success)
        self.assertEqual(customer.cash, 50)           # Баланс наличных обновился
        self.assertEqual(len(customer.cart), 0)       # Корзина очищена после покупки
        self.assertEqual(len(customer.purchase_history), 1)  # История покупок обновлена

    def test_insufficient_funds(self):
        """Проверка ошибки при несоответствии суммы оплаты и стоимости"""
        customer = Customer()
        customer.cart = [Product(0, "Хлеб", 100)]
        success, msg = customer.pay(100, 50, 30, 10)  # Сумма меньше цены товара
        self.assertFalse(success)
        self.assertIn("Сумма не совпадает с общей стоимостью", msg)

    def test_wrong_split(self):
        """Проверка ошибки при превышении средств на оплату отдельными способами"""
        customer = Customer()
        customer.cart = [Product(0, "Хлеб", 100)]
        success, msg = customer.pay(90, 60, 30, 10)
        self.assertFalse(success)
        self.assertIn("Недостаточно средств", msg)

class TestController(unittest.TestCase):
    """Тесты для контроллера: добавление товаров в корзину с разными условиями"""

    def setUp(self):
        """Подготовка контроллера с товарами для тестов"""
        self.controller = Controller()
        self.controller.products = [
            Product(0, "Хлеб", 50),
            Product(1, "Яблоки", 150, requires_weight=True)
        ]

    def test_add_to_cart_simple(self):
        """Добавление простого товара без веса в корзину"""
        success, msg = self.controller.add_to_cart(0)
        self.assertTrue(success)
        self.assertEqual(len(self.controller.customer.cart), 1)

    def test_add_to_cart_requires_weight_missing(self):
        """Попытка добавить товар с весом без указания веса — ошибка"""
        success, msg = self.controller.add_to_cart(1)
        self.assertFalse(success)
        self.assertIn("нужно взвесить", msg)

    def test_add_to_cart_with_weight(self):
        """Добавление товара с весом и проверка правильного расчёта цены"""
        success, msg = self.controller.add_to_cart(1, weight="2")
        self.assertTrue(success)
        product = self.controller.customer.cart[0]
        self.assertEqual(product.weight, 2.0)
        self.assertAlmostEqual(product.price, 300.0)

class TestPayWithProxies(unittest.TestCase):
    """Тесты оплаты через прокси с разными сценариями"""

    def setUp(self):
        """Подготовка контроллера с одним товаром в корзине"""
        self.controller = Controller()
        self.controller.products = [Product(0, "Молоко", 80)]
        self.controller.customer.cart = [self.controller.products[0]]

    def test_underpayment(self):
        """Оплата с недостаточной суммой — отказ"""
        result, msg = self.controller.pay_with_proxies([20, 20, 20])  # 60 < 80
        self.assertFalse(result)
        self.assertIn("Недостаточно средств", msg)

    def test_exact_payment(self):
        """Оплата точной суммой — успешный платёж"""
        result, msg = self.controller.pay_with_proxies([30, 30, 20])  # ровно 80
        self.assertTrue(result)
        self.assertIn("Покупка совершена", msg)

    def test_overpayment(self):
        """Оплата с переплатой — проверка наличия сдачи"""
        result, msg = self.controller.pay_with_proxies([100, 0, 0])  # переплата
        self.assertTrue(result)
        self.assertIn("сдача", msg.lower())
