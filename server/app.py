#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=['GET'])
def restaurants():
    restaurants = []

    for restaurant in Restaurant.query.all():
        restaurant_dict = restaurant.to_dict()
        restaurants.append(restaurant_dict)
    
    response = make_response(
        restaurants,
        200
    )

    return response

@app.route("/restaurants/<int:id>", methods=['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()

    if restaurant is None:
        response_body = {
            "error" : "Restaurant not found"
        }

        response = make_response(
            response_body,
            404
        )
        return response

    else:
        if request.method == 'GET':
            restaurant_dict = restaurant.to_dict()

            response = make_response(restaurant_dict, 200)

            return response
            
        elif request.method == 'DELETE':
            db.session.delete(restaurant)
            db.session.commit()

            response = make_response(
                "",
                200
            )

            return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
