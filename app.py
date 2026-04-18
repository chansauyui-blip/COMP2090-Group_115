from flask import Flask, render_template, request, redirect, url_for, flash
from purchase_system import PurchaseSystem

app = Flask(__name__)
app.secret_key = 'purchase_system_demo_key'
system = PurchaseSystem()

@app.route('/')
def index():
    items = system.get_available_items()
    cart = system.get_cart_items()
    transports = system.get_available_transports()
    subtotal, transport_cost, total = system.calculate_total()
    arrival_dates = system.get_arrival_dates()
    selected_plan_id = system.selected_transport.get_plan_id() if system.selected_transport else None
    has_multiple_sizes = system.has_multiple_sizes()
    ship_separately = system.ship_separately
    return render_template('index.html', 
                           items=items, 
                           cart=cart, 
                           transports=transports,
                           subtotal=subtotal,
                           transport_cost=transport_cost,
                           total=total,
                           arrival_dates=arrival_dates,
                           selected_plan_id=selected_plan_id,
                           has_multiple_sizes=has_multiple_sizes,
                           ship_separately=ship_separately)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = int(request.form['item_id'])
    quantity = int(request.form['quantity'])
    system.add_to_cart(item_id, quantity)
    return redirect(url_for('index', _anchor='cart-section'))

@app.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    system.remove_from_cart(item_id)
    return redirect(url_for('index', _anchor='cart-section'))

@app.route('/set_shipping', methods=['POST'])
def set_shipping():
    separate = request.form.get('separate') == 'yes'
    system.set_shipping_option(separate)
    return redirect(url_for('index', _anchor='transport-section'))

@app.route('/select_transport', methods=['POST'])
def select_transport():
    plan_id = int(request.form['plan_id'])
    system.select_transport(plan_id)
    return redirect(url_for('index', _anchor='summary-section'))

@app.route('/checkout', methods=['POST'])
def checkout():
    success, result = system.checkout()
    if success:
        return render_template('index.html', 
                               order_summary=result,
                               items=system.get_available_items(),
                               cart=[],
                               transports=system.get_available_transports(),
                               subtotal=0,
                               transport_cost=0,
                               total=0,
                               arrival_dates=[],
                               selected_plan_id=None,
                               has_multiple_sizes=False,
                               ship_separately=False)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)