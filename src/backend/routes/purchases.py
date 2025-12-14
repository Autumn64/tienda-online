import os, datetime
from db import Database
from flask import Blueprint, request, jsonify
from interfaces import http_result, decode_token

purchases = Blueprint("purchases", __name__)

def auth_user(token: str) -> dict | None:
    # Sólo los usuarios autenticados pueden ver sus compras.
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

@purchases.route("/", methods=["POST"])
def get_purchases_user():
    # Obtiene todas las compras del usuario autenticado
    auth = request.authorization

    if not auth:
        return http_result(401, message="Se requiere especificar un token.")

    token_user = decode_token(auth.token)

    if not token_user:
        return http_result(401, message="Token inválido.")

    user = auth_user(token_user)

    if not user:
        return http_result(403, message="No tienes permiso para acceder a este recurso.")
    
    response: list = []

    db = Database()

    purchases = db.selectAll({
        "table": "compras",
        "columns": ["id", "monto", "fecha_creacion"],
        "conditions": [
            {
            "prefix": "WHERE",
            "operator": "=",
            "column": "usuario_id",
            "value": int(user["id"])
            }
        ]
    })

    if not purchases:
        return http_result(200, data=response)

    for element in purchases:
        item: dict = {
            "id": element["id"],
            "monto": element["monto"],
            # El campo `fecha_creacion` es de tipo datetime.
            "fecha_compra": element["fecha_creacion"].strftime("%Y-%m-%d %I:%M %p")
        }

        item["productos"] = db.selectAll({
            "table": "productos_compras",
            "columns": ["nombre", "precio", "cantidad", "imagen"],
            "conditions": [
                {
                "prefix": "WHERE",
                "operator": "=",
                "column": "compra_id",
                "value": element["id"]
                }
            ]
        })

        response.append(item)

    db.disconnect()

    return http_result(200, data=response)