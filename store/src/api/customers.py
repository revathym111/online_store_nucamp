from flask import Blueprint, jsonify, abort, request
from ..models import Customer, Contact,db
import hashlib
import secrets
import sqlalchemy

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

customers_bp = Blueprint('customers', __name__, url_prefix = '/customers')

@customers_bp.route('', methods = ['GET']) #decorator takes path and list of HTTP verbs

def index():
    customers = Customer.query.all() #ORM performs SELECT query
    result = []
    for c in customers:
        result.append(c.serialize()) #build list of Customers as dictionary
    return jsonify(result) # return JSN reponse

@customers_bp.route('/<int:id>', methods = ['GET'])
def show(id: int):
    c = Customer.query.get_or_404(id)
    return jsonify(c.serialize())

@customers_bp.route('', methods = ['POST'])
def create():
    # req body must contain username and password
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)
    if len(request.json['username']) < 3 or len(request.json['password']) < 8:
        return abort(400)
    
    # construct Tweet
    c = Customer(
        username = request.json['username'],
        password = scramble(request.json['password']),
        email_id = request.json['email_id'],
        first_name = request.json['first_name'],
        last_name = request.json['last_name'],
        #contact_id = request.json['contact_id']
    )
    db.session.add(c) #prepare CREATE statement
    db.session.commit() #execute CREATE statement

    if 'contact_id' in request.json:
            contact_ids = request.json['contact_id']
            contacts = Contact.query.filter(Contact.contact_id.in_(contact_ids)).all()

            if len(contacts) != len(contact_ids):
                return jsonify({"error": "One or more contact IDs are invalid"}), 400

            c.contacts.extend(contacts)
            db.session.commit()  # Save the contact associations
            
    return jsonify(c.serialize())

@customers_bp.route('/<int:id>', methods = ['DELETE'])
def delete(id: int):
    c =  Customer.query.get_or_404(id)
    try:
        db.session.delete(c) # prepare DELETE statement
        db.session.commit() #execute DELETE statement
        return jsonify(True)
    except:
        #something went wrong :(
        return jsonify(False)

@customers_bp.route('/<int:id>', methods = ['PATCH', 'PUT'])
def update(id:int):
    c = Customer.query.get_or_404(id)
    if 'username' not in request.json and 'password' not in request.json:
        return abort(400)

    if 'username' in request.json:
        c.username = request.json['username']
        if len(c.username) < 3:
            return abort(400)
    
    if 'password' in request.json:
        password = request.json['password']
        if len(password) < 8:
            return abort(400)
        c.password = scramble(password)
    
    try:
        db.session.commit()
        return jsonify(c.serialize()) 

    except:
        return jsonify(False)
    
@customers_bp.route('/<int:id>/customer_contacts', methods=['GET'])
def customer_contacts(id: int):
    c = Customer.query.get_or_404(id)
    result = []
    for cn in c.customer_contacts:
        result.append(cn.serialize())
    return jsonify(result)




