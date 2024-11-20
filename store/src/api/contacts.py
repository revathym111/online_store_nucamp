from flask import Blueprint, jsonify, abort, request
from ..models import Contact, Customer, db

contacts_bp = Blueprint('contacts', __name__, url_prefix='/contacts')


@contacts_bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    contacts = Contact.query.all()  # ORM performs SELECT query
    result = [cont.serialize() for cont in contacts]  # build list of Contacts as dictionaries
    return jsonify(result)  # return JSON response


@contacts_bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    cont = Contact.query.get_or_404(id)
    return jsonify(cont.serialize())


@contacts_bp.route('', methods=['POST'])
def create():
    required_fields = ['customer_id', 'address_line1', 'city', 'state', 'country', 'zip_code', 'phone_number']
    if not all(field in request.json for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Check if customer exists
        customer = Customer.query.get_or_404(request.json['customer_id'])

        # Create the contact and link it to the customer
        cont = Contact(
            address_line1=request.json['address_line1'],
            address_line2=request.json.get('address_line2'),  # Optional field
            city=request.json['city'],
            state=request.json['state'],
            country=request.json['country'],
            zip_code=request.json['zip_code'],
            phone_number=request.json['phone_number']
        )

        # Add the contact to the customer's many-to-many relationship
        customer.contacts.append(cont)

        db.session.add(cont)
        db.session.commit()

        return jsonify(cont.serialize()), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@contacts_bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    cont = Contact.query.get_or_404(id)
    try:
        db.session.delete(cont)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except Exception as e:
        # something went wrong :(
        return jsonify({"error": str(e)}), 400


@contacts_bp.route('/<int:id>/belong_to_customers', methods=['GET'])
def belong_to_customers(id: int):
    cont = Contact.query.get_or_404(id)  # fixed Contact model name
    result = [c.serialize() for c in cont.customers]  # assumes Contact model has a customers relationship
    return jsonify(result)
