from flask import Flask, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from flask_marshmallow import Marshmallow
from datetime import datetime
from typing import List
from sqlalchemy import select, delete, String, ForeignKey
from connection import connection

bp1 = Blueprint('bp1', __name__)
app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:lololo@127.0.0.1/e_com'

db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(16), nullable=False)
    orders = db.relationship('Order', backref= 'customers')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id= db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date= db.Column(db.Date, nullable=False)
    items = db.relationship('OrderItem', backref='order')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(255), nullable=False)
    price= db.Column(db.Float, nullable=False) 
    stock = db. Column(db.Integer, default=0, nullable=False)
    orders = db.relationship('OrderItem', backref='product')


@app.route('/')
def home():
    return "Welcome to Amazon."

#============== CRUD OP TIME BABY LESS GOOO ==========================#
'''

Create (POST)
Retrieve (GET)
Update (PUT)
Delete (DELETE)
'''
########################################




#create
@app.route('/customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    try:
        new_customer = Customer(name = data['name'], email=data['email'], phone_number=data['phone_number'])
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'Message': "New customer added successfully!"}), 201
    except Exception as e:
        return jsonify({'Error': str(e)}), 400



#retrieve
@app.route('/customer/<int:id>', methods= ['GET']) 
def get_customer(id):
   customer = Customer.query.get_or_404(id)
   return jsonify({
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone_number': customer.phone_number
   })

#update
@app.route("/customers/<int:id>", methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    customer = Customer.query.get_or_404(id)
    try:
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone_number = data.get('phone_number', customer.phone_number)
        db.session.commit()
        return jsonify({'message': 'Customer updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

#delete
@app.route("/customers/<int:id>", methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/products/',methods=['POST'], endpoint= 'create_product_bp1')
def create_product():
    data = request.get_json()
    try:
        new_product = Product(name=data['name'], price=data['price'],stock=data['stock'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"Message": 'Product added'})
    except Exception as e:
        return jsonify({'Error': str(e)}), 400

@app.route("/products/<int:id>", methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'stock': product.stock
    })
    
@app.route("/products/<int:id>", methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get_or_404(id)
    try:
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.stock = data.get('stock', product.stock)
        db.session.commit()
        return jsonify({'message': 'Product updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/products/<int:id>", methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route("/orders/",methods=['POST'])
def create_product():
    data = request.get_json()
    try:
        new_order = Order(customer_id=data['customer_id'], date=datetime.utcnow())
        for item in data['products']:
            order_item = OrderItem(order_id=new_order.id, product_id=item['product_id'], quantity=item['quantity'])
            db.session.add(order_item)
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"Message": 'Product added'}), 201
    except Exception as e:
        return jsonify({'Error': str(e)}), 400

@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'stock': p.stock
    } for p in products])


@app.route('/orders/<int:id>', methods=['GET'])
def retrieve_order(id):
    order = Order.query.get_or_404(id)
    items = [{'product_id': i.product_id, 'quantity': i.quantity} for i in order.items]
    return jsonify({
        'id': order.id,
        'customer_id': order.customer_id,
        'date': order.date.isoformat(),
        'items': items
    })

@app.route('/orders/<int:id>/cancel', methods=['PUT'])
def cancel_order(id):
    order = Order.query.get_or_404(id)
    try:
        # Placeholder logic for canceling an order
        return jsonify({'message': 'Order canceled'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug= True)