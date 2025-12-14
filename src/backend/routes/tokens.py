import bcrypt, datetime
from db import Database
from interfaces import http_result, decode_token
from flask import Blueprint, request, jsonify

tokens = Blueprint("tokens", __name__)

@tokens.route("/", methods=["GET"])
# La ruta de este endpoint sería `/api/tokens/`.
def validate_token():
    auth = request.authorization

    if not auth:
        # El cliente debe enviar una cabecera de autorización con el formato
        # `Authorization: Bearer TOKEN`. Idealmente el cliente no enviaría petición alguna
        # si no cuenta con el token, pero igual esta comprobación se agrega como medida de seguridad.
        return http_result(400, message="Se requiere especificar un token.")

    token_user = decode_token(auth.token)

    if not token_user:
        return http_result(404, message="Token inválido.")

    db = Database()

    user = db.selectOne({
        "table": "usuarios",
        "columns": ["username", "tipo", "verificado"],
        "conditions": [
            {
            "prefix": "WHERE",
            "operator": "=",
            "column": "username",
            "value": token_user["username"]
            },
            {
            "prefix": "AND",
            "operator": "=",
            "column": "eliminado",
            "value": False
            }
        ]
    })

    db.disconnect()

    if not user: 
        return http_result(404, "fail", message="Token inválido.")
    

    return http_result(200, data={
        "type": user["tipo"],
        "verificado": user["verificado"]
    })