import bcrypt
from db import Database
from interfaces import http_result, gen_token
from flask import Blueprint, request, jsonify

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if None in [email, password]:
        return http_result(400, "fail", message="Se requiere especificar un correo y una contraseña.")

    db = Database()

    user = db.selectOne({
        "table": "usuarios",
        "columns": ["id", "username", "passwd", "tipo", "eliminado"],
        "condition": {
            "operator": "=",
            "column": "email",
            "value": email
        }
    })

    if not user or user["eliminado"]:
        db.disconnect()
        return http_result(404, "fail", message="Usuario o contraseña incorrecta.")
    
    if not bcrypt.checkpw(password.encode(), user["passwd"].encode()):
        db.disconnect()
        return http_result(401, "fail", message="Usuario o contraseña incorrecta.")

    newToken = gen_token()

    db.insertData({
        "table": "tokens",
        "columns": ["usuario_id", "token", "fecha_creacion", "fecha_expiracion"],
        "values": [user["id"], newToken["hash_token"], newToken["creation_date"], newToken["expiration_date"]]
    })

    db.disconnect()

    return http_result(200, "success", 
        data={
            "username": user["username"],
            "type": user["tipo"],
            "token": newToken["token"]
    })