from db import Database
from emails import Email
import bcrypt, os, datetime
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

@auth.route("/signup", methods=["POST"])
# La ruta de este endpoint sería `/api/auth/signup`
def singup():
    # Realiza el registro del usuario. No verifica si el correo existe, por lo que se asume
    # que el usuario siempre va a introducir un correo electrónico válido.
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if None in [username, email, password]:
        return http_result(400, message="Se requiere especificar un usuario, un correo y una contraseña.")
    
    if len(password) < 8:
        return http_result(400, message="La contraseña debe tener mínimo 8 caracteres.")

    db = Database()

    user = db.selectOne({
        "table": "usuarios",
        "columns": ["id"],
        "conditions": [
            {
            "prefix": "WHERE",
            "operator": "=",
            "column": "email",
            "value": email
            },
            {
            "prefix": "OR",
            "operator": "=",
            "column": "username",
            "value": username
            }
        ]
    })

    if user:
        db.disconnect()
        return http_result(400, message="Un usuario ya se registró previamente con ese nombre de usuario o con ese correo.")

    # Hashea la contraseña con 14 rondas.
    hashed_passwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))

    rows = db.insertOne({
        "table": "usuarios",
        "columns": ["username", "email", "passwd", "tipo", "verificado", "eliminado", "fecha_creacion"],
        "values": [username, email, hashed_passwd.decode(), "cliente", True, False, datetime.datetime.now()]
    })

    db.disconnect()

    if not rows:
        return http_result(500, message="No se pudo completar el registro.")

    # Envía correo electrónico de bienvenida.
    mailServer = Email(
        server=os.getenv("MAIL_SERVER"),
        port=int(os.getenv("MAIL_PORT")),
        user=os.getenv("MAIL_USER"),
        password=os.getenv("MAIL_PASS")
    )

    mailServer.sendMessage(email, "Bienvenida Tienda Online", f"Te damos la bienvenida a Tienda Online UVM.", "text")
    mailServer.quit()

    return http_result(201, message="Registro completado exitosamente. Ahora puede iniciar sesión.")