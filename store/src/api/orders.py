from flask import Blueprint, jsonify, abort, request
from ..models import Order, Customer, db
import datetime
import pytz

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    orders = Order.query.all()  # ORM performs SELECT query
    result = [ord.serialize() for ord in orders]  # build list of Orders as dictionaries
    return jsonify(result)  # return JSON response


@orders_bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    ord = Order.query.get_or_404(id)
    return jsonify(ord.serialize())


@orders_bp.route('', methods=['POST'])
def create():
    required_fields = ['customer_id']
    if not all(field in request.json for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Check if customer exists
        customer = Customer.query.get_or_404(request.json['customer_id'])

        # Handle order_date_time: If it's not passed, use UTC now
        order_date_time = request.json.get('order_date_time')
        if order_date_time:
            # Ensure the incoming order_date_time is timezone-aware (parse it if needed)
            order_date_time = datetime.datetime.fromisoformat(order_date_time).astimezone(pytz.UTC)
        else:
            # Default to UTC now if not provided
            order_date_time = datetime.datetime.utcnow().astimezone(pytz.UTC)

        # Create the order and link it to the customer
        ord = Order(
            customer_id = request.json['customer_id'],
            order_date_time=order_date_time  # Optional field
        )

        db.session.add(ord)
        db.session.commit()

        return jsonify(ord.serialize()), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@orders_bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    ord = Order.query.get_or_404(id)
    try:
        db.session.delete(ord)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify({"success": True}), 200
    except Exception as e:
        # something went wrong :(
        return jsonify({"error": str(e)}), 400


@orders_bp.route('/<int:id>/customer_orders', methods=['GET'])
def customer_orders(id: int):
    customer = Customer.query.get_or_404(id)  # fetch customer by ID
    result = [o.serialize() for o in customer.orders]  # Serialize orders
    return jsonify(result)
