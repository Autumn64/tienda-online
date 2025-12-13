import os, stripe
from db import Database
from decimal import Decimal, ROUND_HALF_UP
from flask import Blueprint, request, jsonify
from interfaces import http_result, decode_token

checkout = Blueprint("checkout", __name__)

stripe.api_key = os.getenv("STRIPE_KEY")

def auth_user(token: str) -> dict | None:
    # Sólo los usuarios autenticados pueden hacer la compra.
    db = Database()

    user = db.selectOne({
        "table": "usuarios",
        "columns": ["id", "tipo"],
        "conditions": [
            {
            "prefix": "WHERE",
            "operator": "=",
            "column": "username",
            "value": token["username"]
            }
        ]
    })

    db.disconnect()

    return user

def to_stripe_amount(value: Decimal) -> int:
    return int((value * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

def get_line_items(products):
    line_items: list = []
    db = Database()
    
    for element in products:
        newProduct = db.selectOne({
            "table": "productos",
            "columns": ["nombre", "precio"],
            "conditions": [
                {
                "prefix": "WHERE",
                "operator": "=",
                "column": "id",
                "value": element["id"]
                },
                {
                "prefix": "AND",
                "operator": "=",
                "column": "eliminado",
                "value": False
                }
            ]
        })

        if not newProduct: continue

        unit_amount = to_stripe_amount(newProduct["precio"])

        line_items.append({
            "price_data": {
                "currency": "mxn",
                "unit_amount": unit_amount,
                "product_data": {
                    "name": newProduct["nombre"],
                    "metadata": {
                        "product_id": element["id"]
                    }
                }
            },
            "quantity": element["qty"]
        })
    
    db.disconnect()
    
    return line_items


@checkout.route("/", methods=["POST"])
def create_checkout_session():
    auth = request.authorization

    if not auth:
        return http_result(401, message="Se requiere un token válido.")

    token_user = decode_token(auth.token)

    if not token_user:
        return http_result(401, message="Token inválido.")

    user = auth_user(token_user)

    if not user:
        return http_result(401, message="Sólo los usuarios autenticados pueden hacer compras.")

    if not request.is_json:
        return http_result(400, message="Sólo se acepta información en formato JSON.")

    data = request.json

    line_items: list = get_line_items(data["cart"].values())

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=line_items,
        success_url="http://localhost/tienda-online",
        cancel_url=data["backurl"]
    )

    return http_result(202, data={
        "id": session.id,
        "url": session.url
    })