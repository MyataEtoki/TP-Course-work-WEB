from flask import render_template, request, redirect, url_for, session, flash
from app import create_app
from app.controllers import Controller
from app.commands import PayCommand

app = create_app()
controller = Controller()

@app.route('/')
def index():
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
        total=controller.customer.total_cart()  # ← добавили итоговую сумму
    )


@app.route('/add', methods=["POST"])
def add():
    index = int(request.form['product_index'])
    weight = request.form.get('weight', None)
    success, msg = controller.add_to_cart(index, weight)
    flash(msg)
    return redirect(url_for('index'))

@app.route('/remove/<int:index>')
def remove(index):
    controller.remove_from_cart(index)
    return redirect(url_for('index'))

@app.route('/buy', methods=['POST'])
def buy():
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
    msg = controller.customer.go_to_work()
    flash(msg)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
