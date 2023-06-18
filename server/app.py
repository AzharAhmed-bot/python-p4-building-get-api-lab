#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_cakes=BakedGood.query.all()
    cakes=[]
    for cake in all_cakes:
        cake_dict={
            "bakery_id":cake.bakery_id,
            "created_at":cake.created_at,
            "id":cake.id,
            "name":cake.name,
            "price":cake.price,
            "updated_at":cake.updated_at
        }
        cakes.append(cake_dict)
    response=make_response(jsonify(cakes),200)
    response.headers["Content_Type"]="application/json"
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        bakery_dict = bakery.to_dict()
        response = make_response(jsonify(bakery_dict), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        # Handle the case when the bakery with the given id is not found
        response = make_response(jsonify({"error": "Bakery not found"}), 404)
        response.headers["Content-Type"] = "application/json"
        return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_list = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_item = [cake.to_dict() for cake in baked_list]
    response = make_response(jsonify(baked_item), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    response = make_response(jsonify(most_expensive.to_dict()), 200)
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
