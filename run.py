from flask import render_template, request, redirect, url_for, session, flash
from app import create_app
from app.controllers import StoreController

app = create_app()
controller = StoreController()

@app.route('/')
def index():
    return render_template("index.html", products=controller.get_products(), cart=controller.get_cart())

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

@app.route('/buy', methods=["POST"])
def buy():
    try:
        cash = float(request.form['cash'])
        card = float(request.form['card'])
        bonus = float(request.form['bonus'])
    except ValueError:
        flash("Введите корректные значения")
        return redirect(url_for('index'))

    success, msg = controller.attempt_purchase(cash, card, bonus)
    flash(msg)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
