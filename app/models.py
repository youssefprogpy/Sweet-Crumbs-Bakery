import bcrypt
from app.extentions import db, login_manager
from datetime import datetime
from flask_login import UserMixin


# creating models/tables in database
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    oauth_provider = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship("Order", back_populates="user")

    # method of hashing(binary level so encode/decode('utf-8') is mendatory)
    # making static method in order to get rid of of instance dependacy
    @staticmethod
    def hashing_pass(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # method of checking the hashed_password
    @staticmethod
    def check_hash(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


# function to load user id from database for cookies
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(
        int(user_id)
    )  # the int method is necessary here since flask login stores id in session as string while id in db is integer


class Category(db.Model):
    # table name
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    products = db.relationship("Product", back_populates="category")


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    image_url = db.Column(db.String(70))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.relationship("Category", back_populates="products")
    order_items = db.relationship("OrderItem", back_populates="product")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), default="pending")
    total_price = db.Column(db.Numeric(6, 2), nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order")


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(6, 2), nullable=False)
    order = db.relationship("Order", back_populates="order_items")
    product = db.relationship("Product", back_populates="order_items")


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
