from flask import render_template, request, redirect, url_for, session, flash
from app import create_app
from app.controllers import Controller
from app.commands import PayCommand

# Инициализация Flask-приложения и основного контроллера
app = create_app()
controller = Controller()

@app.route('/')
def index():
    """
    Главная страница.
    Отображает список товаров, корзину, баланс и историю покупок.
    """
    return render_template(
        "index.html",
        products=controller.get_products(),
        cart=controller.get_cart(),
        history=controller.customer.purchase_history,
        balance={
            "cash": controller.customer.cash,
            "card": controller.customer.card,
            "bonus": controller.customer.bonus
        },
        total=controller.customer.total_cart()
    )

@app.route('/add', methods=["POST"])
def add():
    """
    Обработка добавления товара в корзину.
    Учитывает вес, если он требуется.
    """
    index = int(request.form['product_index'])
    weight = request.form.get(f'weight_{index}', None)
    success, msg = controller.add_to_cart(index, weight)
    flash(msg)
    return redirect(url_for('index'))

@app.route('/remove/<int:index>')
def remove(index):
    """
    Удаляет товар из корзины по его индексу.
    """
    controller.remove_from_cart(index)
    return redirect(url_for('index'))

@app.route('/buy', methods=['POST'])
def buy():
    """
    Обрабатывает оплату покупки.
    Использует паттерн 'Команда'.
    """
    amounts = [
        request.form.get('cash', '0'),
        request.form.get('card', '0'),
        request.form.get('bonus', '0')
    ]
    cmd = PayCommand(controller, amounts)
    success, msg = cmd.execute()
    flash(msg)
    return redirect(url_for('index'))

@app.route('/work')
def work():
    """
    Добавляет пользователю деньги и бонусы.
    Симулирует 'поход на работу'.
    """
    success, msg = controller.customer.go_to_work()
    flash(msg)
    return redirect(url_for('index'))

if __name__ == "__main__":
    """
    Запуск сервера Flask в режиме отладки.
    """
    app.run(debug=True)
