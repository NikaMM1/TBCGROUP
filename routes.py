from flask import render_template, redirect, url_for, flash, session, current_app, request
from flask_login import login_user, logout_user, login_required, current_user
from ext import app, db, login_manager
from models import User, Order, MenuItem  # Ensure MenuItem is imported from models if it's defined there
from forms import RegisterForm, LoginForm, OrderForm

menu_items = [
    MenuItem(1, 'Pizza', 'Delicious pizza with cheese and toppings', 12.99, 'pizza.jpg'),
    MenuItem(2, 'Burger', 'Juicy burger with fries', 8.99, 'burger.jpg'),
    MenuItem(3, 'Salad', 'Fresh garden salad', 7.99, 'salad.jpg'),
    MenuItem(4, 'Pasta', 'Spaghetti with marinara sauce', 10.99, 'pasta.jpg'),
    MenuItem(5, 'Sandwich', 'Classic ham and cheese sandwich', 6.99, 'sandwich.jpg'),
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html', menu_items=menu_items)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists', 400
        register_user(username, password)
        return 'User registered successfully', 201
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    form = OrderForm()
    if form.validate_on_submit():
        new_order = Order(
            email=form.email.data,
            address=form.address.data,
            card_number=form.card_number.data,
            food_item=form.food_item.data,
            card_name=form.card_name.data,
            expiration_date=form.expiration_date.data,
            cvv=form.cvv.data
        )
        db.session.add(new_order)
        db.session.commit()
        session.pop('cart', None)
        flash('Order submitted successfully.')
        return redirect(url_for('index'))
    cart_items = session.get('cart', [])
    current_app.logger.info(f"Cart items before rendering order.html: {cart_items}")
    return render_template('order.html', form=form, cart_items=cart_items)

@app.route('/admin/orders')
@login_required
def admin_orders():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('index'))
    orders = Order.query.all()
    return render_template('admin_orders.html', orders=orders)

@app.route('/admin/orders/delete/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('index'))
    order = Order.query.get(order_id)
    if order:
        db.session.delete(order)
        db.session.commit()
        flash('Order deleted successfully.')
    return redirect(url_for('admin_orders'))

@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    item = next((item for item in menu_items if item.id == item_id), None)
    if not item:
        return 'Item not found', 404
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append({
        'name': item.name,
        'description': item.description,
        'price': item.price,
        'image_url': item.image_url
    })
    flash(f"{item.name} added to cart successfully.")
    return redirect(url_for('menu'))

def register_user(username, password):
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
