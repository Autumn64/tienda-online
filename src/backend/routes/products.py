import os
from db import Database
from flask import Blueprint, request, jsonify

products = Blueprint("products", __name__)

def auth_user(token: str) -> dict | None:
    db = Database()

    user = db.selectOne({
        "table": "usuarios",
        "columns": ["username", "tipo"],
        "conditions": [
            {
            "prefix": "WHERE",
            "operator": "=",
            "column": "username",
            "value": token_user["username"]
            }
        ]
    })

    db.disconnect()

    if not user or user["tipo"] != "admin": 
        return None

    return user

@products.route("/<product_id>", methods=["GET"])
def get_product(product_id):
    db = Database()
    # Aquí se hace la consulta SQL con `selectOne()` y usando la variable `product_id`
    # La consulta debe hacerse sobre la vista `categorias-productos` usando el ID del producto.


    # Aquí se hace la respuesta, si el resultado de la consulta es None
    # responde con estatus 404, de lo contrario responde con estatus 200.

@products.route("/<product_id>", methods=["POST"])
def create_product(product_id):
    auth = request.authorization

    if not auth:
        return http_result(400, message="Se requiere especificar un token.")

    token_user = decode_token(auth.token)

    if not token_user:
        return http_result(404, message="Token inválido.")

    user = auth_user(token_user)

    if not user:
        return http_result(403, message="No tienes permiso para acceder a este recurso.")

    db = Database()

    # Aquí se hace una consulta SELECT para verificar si el producto ya existe.

    # Si el producto ya existe, el servidor debe responder con estatus 400.

    # Aquí se hace la consulta INSERT, mediante `insertOne()`.

    # Aquí se hace la respuesta del servidor (estatus 201).