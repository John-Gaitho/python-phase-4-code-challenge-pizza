from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    # Relationship
    restaurant_pizzas = db.relationship(
        "RestaurantPizza",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )

    # serialization rules
    serialize_rules = ("-restaurant_pizzas",)

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    # Relationship
    restaurant_pizzas = db.relationship(
        "RestaurantPizza",
        back_populates="pizza"
    )

    # add serialization rules
    # Serialization rules
    serialize_rules = ("-restaurant_pizzas",)

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"
class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships

    # add serialization rules

    # add validation
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"), nullable=False)

    # Relationships
    restaurant = db.relationship(
        "Restaurant",
        back_populates="restaurant_pizzas"
    )
    pizza = db.relationship(
        "Pizza",
        back_populates="restaurant_pizzas"
    )

    # Serialization rules
    serialize_rules = ("-restaurant.restaurant_pizzas", "-pizza.restaurant_pizzas")

    # Validation
    @validates("price")
    def validate_price(self, key, value):
        if not 1 <= value <= 30:
            raise ValueError("Price must be between 1 and 30")
        return value

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"