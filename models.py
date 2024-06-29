from ext import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, )
    password_hash = db.Column(db.String(128), )
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True  

    def is_active(self):
        return True     

    def is_anonymous(self):
        return False 
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), )
    address = db.Column(db.String(150), )
    food_item = db.Column(db.String(50),)
    card_number = db.Column(db.String(20),)
    card_name = db.Column(db.String(150), )
    expiration_date = db.Column(db.String(10),)
    cvv = db.Column(db.String(4), )
    cart_items = db.relationship('OrderItem', backref='order', lazy=True)

class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),)
    description = db.Column(db.Text)
    price = db.Column(db.Float,)
    image_url = db.Column(db.String(256))
class OrderItem(db.Model):
    __tablename__ = 'order_items'  
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'),)  
    name = db.Column(db.String(128),)
    description = db.Column(db.String(256),)
    price = db.Column(db.Float, )
    image_url = db.Column(db.String(256), )
    



    