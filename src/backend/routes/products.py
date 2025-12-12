import os
from db import Database
from interfaces import http_result
from flask import Blueprint, request, jsonify

products = Blueprint("products", __name__)

def auth_user(token: str) -> dict | None:
    # Autenticación específicamente para las operaciones CUD.
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

@products.route("/", methods=["GET"])
def get_products():
    # Despliega todos los productos disponibles.
    db = Database()

    products = db.selectAll({
        "table": "tarjetas_productos",
        "columns": ["*"]
    })

    db.disconnect()

    if not products:
        return http_result(404, message="No se encontraron productos.")

    return http_result(200, data=products)

@products.route("/<product_id>", methods=["GET"])
def get_product(product_id):
    # Despliega la información del producto seleccionado, junto con sus imágenes
    db = Database()

    product = db.selectOne({
        "table": "productos",
        "columns": ["nombre", "precio", "descripcion", "stock"],
        "conditions": [
            {
            "prefix": "WHERE",
            "operator": "=",
            "column": "id",
            "value": product_id
            }
        ]
    })

    if not product:
        db.disconnect()
        return http_result(404, message="No se encontró el producto seleccionado.")
    
    images = db.selectAll({
        "table": "imagenes",
        "columns": ["ruta"],
        "conditions": [
            {
            "prefix": "WHERE",
            "operator": "=",
            "column": "producto_id",
            "value": product_id
            }
        ]
    })

    db.disconnect()

    product["imagenes"] = []

    for element in images:
        product["imagenes"].append(element["ruta"])

    return http_result(200, data=product)

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