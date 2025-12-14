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
        "columns": ["id"],
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
    # Stripe no lee decimales, sino números enteros, de los cuales toma
    # los últimos dos dígitos para los centavos.
    return int((value * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

def get_line_items(products):
    # Obtiene los items del carrito, y obtiene su nombre y su precio. Después,
    # crea una lista con la información tal y como la va a leer Stripe.
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
                "operator": ">",
                "column": "stock",
                "value": 0
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
                        "product_id": element["id"],
                    }
                }
            },
            "quantity": element["qty"]
        })
    
    db.disconnect()
    
    return line_items


@checkout.route("/", methods=["POST"])
def create_checkout_session():
    # Recibe el carrito de compras en formato JSON, y crea una sesión de Stripe
    # para realizar el pago.
    if not request.is_json:
        return http_result(400, message="Sólo se acepta información en formato JSON.")

    auth = request.authorization

    if not auth:
        return http_result(401, message="Se requiere un token válido.")

    token_user = decode_token(auth.token)

    if not token_user:
        return http_result(401, message="Token inválido.")

    user = auth_user(token_user)

    if not user:
        return http_result(401, message="Sólo los usuarios autenticados pueden hacer compras.")

    data = request.json

    line_items: list = get_line_items(data["cart"].values())

    # Esta es la sesión de stripe, cuya URL se envía al cliente para acceder a
    # la pantalla de pago.
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=line_items,
        metadata={
            "user_id": str(user["id"])
        },
        success_url="http://store.autumn64.xyz/tienda-online/purchase_success.html",
        cancel_url=data["backurl"]
    )

    return http_result(202, data={
        "id": session.id,
        "url": session.url
    })