import datetime
import os, stripe
from db import Database
from flask import Blueprint, request, jsonify
from interfaces import http_result

webhooks = Blueprint("webhooks", __name__)

stripe.api_key = os.getenv("STRIPE_KEY")
endpoint_key = os.getenv("STRIPE_WEBHOOK_KEY")

def complete_checkout(session):
    # Primero obtiene los productos de la sesión (porque el webhook no los proporciona),
    # y en la BD inserta la compra y las transacciones de cada producto. Después,
    # reduce el stock de cada producto con base en la cantidad que se compró.
    session_id = session["id"]
    line_items = stripe.checkout.Session.list_line_items(
        session_id,
        expand=["data.price.product"],
        limit=100
    )

    db = Database()

    user_id = session["metadata"]["user_id"]
    total_price = int(session["amount_total"]) / 100

    newPurchase = db.insertOne({
        "table": "compras",
        "columns": ["usuario_id", "monto", "fecha_creacion"],
        "values": [user_id, total_price, datetime.datetime.now()]
    })

    for element in line_items["data"]:
        quantity = element["quantity"]
        # Así de profunda está esta información a partir de la respuesta de Stripe.
        product_id = element["price"]["product"]["metadata"]["product_id"]

        # Obtiene el stock original del producto.
        # Es mejor hacer la actualización directamente: `stock = stock - quantity`,
        # pero ello implicaría reimplementar la interfaz Database, para lo cual
        # ya no nos queda tiempo; por eso lo hicimos así.
        og_stock = db.selectOne({
            "table": "productos",
            "columns": ["stock"],
            "conditions": [
                {
                    "prefix": "WHERE",
                    "operator": "=",
                    "column": "id",
                    "value": product_id
                }
            ]
        })

        db.insertOne({
            "table": "transacciones",
            "columns": ["producto_id", "compra_id", "cantidad"],
            "values": [product_id, newPurchase, quantity]
        })

        db.updateRows({
            "table": "productos",
            "columns": ["stock"],
            "values": [int(og_stock["stock"]) - quantity],
            "conditions": [
                {
                "prefix": "WHERE",
                "operator": "=",
                "column": "id",
                "value": product_id
                },
                {
                "prefix": "AND",
                "operator": ">",
                "column": "stock",
                "value": 0
                }
            ]
        })
    
    db.disconnect()

    return http_result(200)

@webhooks.route("/", methods=["POST"])
def stripe_webhook():
    # Webhook que recibe los eventos de Stripe.
    sig_header = request.headers.get("Stripe-Signature")

    if not sig_header or not endpoint_key:
        return http_result(400)

    payload = request.data

    # Esto es de mismo Stripe, y es para obtener el evento que se recibió.
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_key
        )
    except ValueError:
        return http_result(400)
    except stripe.error.SignatureVerificationError:
        return http_result(400)

    # No hace nada si la compra no se completó.
    if event["type"] != "checkout.session.completed":
        return http_result(204)

    return complete_checkout(event["data"]["object"])