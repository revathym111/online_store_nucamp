# Import libraries for working with dates and SQLAlchemy
import datetime
from pytz import timezone
from flask_sqlalchemy import SQLAlchemy

# Create an instance of SQLAlchemy to manage the database connection
db = SQLAlchemy()

# Define the association table for customers and contacts (many-to-many relationship)
customers_contacts = db.Table(
    'customers_contacts',
    # Define columns for customer ID (foreign key to customer.id)
    db.Column(
        'customer_id', db.Integer,
        db.ForeignKey('customers.customer_id'),
        primary_key=True
    ),
    # Define columns for contact ID (foreign key to contact.id)
    db.Column(
        'contact_id', db.Integer,
        db.ForeignKey('contacts.contact_id'),
        primary_key=True
    ),
)

# Define the Customer model
class Customer(db.Model):
    __tablename__ = 'customers'  # Set the table name in the database

    # Define the Customer model columns
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique ID (auto-increments)
    username = db.Column(db.String(128), unique=True, nullable=False)  # Username (unique, not null)
    password = db.Column(db.String(128), nullable=False)  # Password (not null)
    email_id = db.Column(db.String(128), nullable=False, unique=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    
    # Define a relationship with the Contact model
    '''contacts = db.relationship(
        'Contact', secondary=customers_contacts,
        backref=db.backref('customers', lazy='dynamic'), cascade="all, delete"
    )'''
    contacts = db.relationship(
        'Contact', secondary=customers_contacts, back_populates='customers'
    )

    # Define a relationship with the Orders model
    orders = db.relationship('Order', back_populates='customer', cascade="all,delete")

    # Define a constructor for the Customer model
    def __init__(self, username: str, password: str, email_id: str, first_name: str, last_name: str):
        self.username = username
        self.password = password
        self.email_id = email_id
        self.first_name = first_name
        self.last_name = last_name

    # Define a method to serialize the Customer object as a dictionary
    def serialize(self):
        return {
            #'id': self.customer_id,
            'username': self.username,
            'email_id': self.email_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'contacts' : [contact.contact_id for contact in self.contacts]
        }

# Define the Contacts model
class Contact(db.Model):
    __tablename__ = 'contacts'  # Set the table name in the database

    # Define the Contact model columns
    contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique ID (auto-increments)
    address_line1 = db.Column(db.String(280), nullable=False)  # Contact address (not null, max 280 chars)
    address_line2 = db.Column(db.String(280))
    city = db.Column(db.String(280), nullable=False)
    state = db.Column(db.String(280), nullable=False)
    country = db.Column(db.String(280), nullable=False)
    zip_code = db.Column(db.String(280), nullable=False)
    phone_number = db.Column(db.String(280), nullable=False, unique=True)

    # Define a relationship with the Customer model (many-to-many through customers_contacts)
    customers = db.relationship(
        'Customer', secondary=customers_contacts, back_populates='contacts'
    )

    # Define a constructor for the Contacts model
    def __init__(self, address_line1: str, address_line2: str, city: str, state: str, country: str, zip_code: str, phone_number: str):
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.city = city
        self.state = state
        self.country = country
        self.zip_code = zip_code
        self.phone_number = phone_number

    # Define a method to serialize the Contact object as a dictionary
    def serialize(self):
        return {
            'id': self.contact_id,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'zip_code': self.zip_code,
            'phone_number': self.phone_number,
            'customers' : [customer.customer_id for customer in self.customers]
        }

# Define the Orders model
class Order(db.Model):
    __tablename__ = 'orders'  # Set the table name in the database

    # Define the Order model columns
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    order_date_time = db.Column(
        db.DateTime(timezone=True),
        default=datetime.datetime.utcnow
    )  # Creation timestamp with timezone (defaults to UTC now)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)  
    # Define a relationship with the Customer model (one-to-many from Customer to Order)
    customer = db.relationship(
        'Customer',
        back_populates='orders'  # Back-reference relationship
    )

    # Define a constructor for the Order model
    def __init__(self, order_date_time: datetime.datetime, customer_id: int):
        self.order_date_time = order_date_time
        self.customer_id = customer_id

    # Define a method to serialize the Order object as a dictionary
    def serialize(self):
        return {
            'id': self.order_id,
            'order_date_time': self.order_date_time.isoformat(), # Serialize as ISO format string
            'customer_id': self.customer_id
        }

# Define the Products model
class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique ID (auto-increments)
    product_name = db.Column(db.String(128), nullable=False)  
    description = db.Column(db.String(250))
    stock_quantity = db.Column(db.Integer, nullable=False)
  
    order_item_id = db.Column(db.Integer, db.ForeignKey('orderitems.order_item_id'), nullable=False)  
    
    # Define a constructor for the Products model
    def __init__(self, product_name: str, description: str, stock_quantity: int, order_item_id: int):
        self.product_name = product_name
        self.description = description
        self.stock_quantity = stock_quantity
        self.order_item_id = order_item_id

    # Define a method to serialize the product object as a dictionary
    def serialize(self):
        return {
            'id': self.product_id,
            'product_name': self.product_name,
            'description': self.description,
            'stock_quantity': self.stock_quantity,
            'order_item_id': self.order_item_id
        }
    
# Define the Orderitems model
class Orderitem(db.Model):
    __tablename__ = 'orderitems'

    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_quantity = db.Column(db.Integer)
    
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    orders = db.relationship(
        'Order',
        backref='orderitems'  # Back-reference relationship
    )
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    products = db.relationship(
        'Product',
        backref='orderitems',  # Back-reference relationship
        foreign_keys=[product_id]  # Explicitly specify the foreign key
    )

    def __init__(self, item_quantity: int, order_id: int, product_id: int):
        self.item_quantity = item_quantity
        self.order_id = order_id
        self.product_id = product_id

    def serialize(self):
        return {
            'id': self.order_item_id,
            'item_quantity': self.item_quantity,
            'order_id': self.order_id,
            'product_id': self.product_id
        }

