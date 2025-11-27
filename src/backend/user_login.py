import bcrypt
from db import Database
from interfaces import http_result
from flask import Blueprint, request, jsonify

user_login = Blueprint("user_login", __name__)

@user_login.route("", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return http_result(400, "fail", message="Se requieren un usuario y una contraseña")
    
    db = Database()

    query = "SELECT username, passwd, tipo, eliminado FROM usuarios WHERE email=%s"

    user = db.selectOne(query, [data["email"]])

    if not user:
        return http_result(404, "fail", message="El usuario no existe")
    
    if not bcrypt.checkpw(data["password"].encode(), user["passwd"].encode()):
        return http_result(401, "fail", message="Contraseña incorrecta")

    del user["passwd"]

    if user["eliminado"]:
        return http_result(404, "fail", message="El usuario no existe")
    

    return http_result(200, "success", data=user)