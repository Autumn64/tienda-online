import bcrypt, datetime
from db import Database
from interfaces import http_result, get_token_user
from flask import Blueprint, request, jsonify

tokens = Blueprint("tokens", __name__)

@tokens.route("/", methods=["POST"])
def validate_token():
    data = request.get_json()
    token = data.get("token")

    if not token:
        return http_result(400, "fail", message="Se requiere especificar un token.")

    db = Database()

    hash_tokens = db.selectAll({
        "table": "tokens",
        "columns": ["usuario_id", "token"],
        "condition": {
            "operator": ">",
            "column": "fecha_expiracion",
            "value": datetime.datetime.now()
        }
    })

    db.disconnect()

    if not hash_tokens: 
        return http_result(404, "fail", message="Token no encontrado.")
    
    user = get_token_user(hash_tokens, token)

    if not user:
        return http_result(404, "fail", message="Token no encontrado.")

    return http_result(200, "success", 
        data={
            "username": user
    })