import bcrypt, os
from db import Database
from emails import Email
from flask import Blueprint, request, jsonify
from interfaces import http_result, gen_token, gen_tfa_code

auth = Blueprint("auth", __name__)
tfaCodes = {}

@auth.route("/login", methods=["POST"])
# La ruta de este endpoint sería `/api/auth/login`.
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    authCode = data.get("auth")

    if None in [email, password]:
        # Si cualquiera de los dos está vacío o es nulo, se devuelve bad request.
        return http_result(400, message="Se requiere especificar un correo y una contraseña.")

    db = Database()

    user = db.selectOne({
        "table": "usuarios",
        "columns": ["id", "username", "passwd", "tipo"],
        "conditions": [
            {
            "prefix": "WHERE",
            "operator": "=",
            "column": "email",
            "value": email
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
        return http_result(404, message="Usuario o contraseña incorrecta.")
    
    if not bcrypt.checkpw(password.encode(), user["passwd"].encode()):
        # Verifica la contraseña introducida con el hash que está en la base de datos.
        return http_result(401, message="Usuario o contraseña incorrecta.")

    if not authCode:
        # Si no se incluyó el código de verificación en la petición, se genera uno y notifica al cliente.
        tfaCode = gen_tfa_code()
        tfaCodes[user["username"]] = tfaCode
        mailServer = Email(
            server=os.getenv("MAIL_SERVER"),
            port=int(os.getenv("MAIL_PORT")),
            user=os.getenv("MAIL_USER"),
            password=os.getenv("MAIL_PASS")
        )

        mailServer.sendMessage(email, "Código 2FA Tienda Online", f"Tu código de verificación es {tfaCode}.", "text")
        mailServer.quit()
        return http_result(202, message=f"Introduce el código de verificación enviado a `{email}`.")

    if authCode != tfaCodes[user["username"]]:
        # Si el código generado y el código que introdujo el usuario no coinciden, se impide
        # el inicio de sesión.
        return http_result(401, message="Código de verificación incorrecto.")

    # Limpia el token para que no se pueda reutilizar
    del tfaCodes[user["username"]]
    
    # Genera el token de sesión
    newToken: str = gen_token({"username": user["username"]})

    return http_result(200, data={"token": newToken})