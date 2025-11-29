import datetime, jwt, os
from flask import jsonify

SUCCESS_CODES = {200, 201, 202, 204}
FAIL_CODES = {400, 401, 404, 405}
ERROR_CODES = {500}

def get_status(code: int) -> str:
    # Genera automáticamente el estatus de la respuesta con base en la especificación acordada.
    if code in SUCCESS_CODES: return "success"
    if code in FAIL_CODES: return "fail"
    if code in ERROR_CODES: return "error"

    raise Exception(f"{code} is not a valid status code.")

def http_result(code: int, data: dict = None, message: str = None):
    # Genera la respuesta del servidor en formato JSON con base en las especificaciones acordadas.
    # Un ejemplo de respuesta válida es el siguiente:
    # {
    #     "code": 200,
    #     "status": "success",
    #     "message": "Login correcto",
    #     "data": {
    #         "username": "autumn64",
    #         "type": "admin"
    #     }
    # }
    # Los parámetros `data` y `message` son opcionales, si bien debería incluirse al menos uno en la
    # respuesta para mantener la consistencia en la API.
    # `message` está destinado a mensajes que se muestren directamente al usuario o que provoquen 
    # una acción en el cliente, mientras que `data` es para información que el cliente debe procesar
    # y desplegar.
    # Hay que tomar en cuenta que se deben especificar explícitamente los parámetros `data` y `message`, 
    # ya que de no hacerlo Python no sabe diferenciarlos y termina enviando una respuesta 
    # diferente a la que originalmente queríamos enviar.

    result = {
        "code": code,
        "status": get_status(code)
    }

    if data is not None: result["data"] = data
    if message is not None and message.strip() != "": result["message"] = message

    return jsonify(result), code

def gen_token(data: dict, expiration: datetime.date = None) -> str:
    # Genera un token JWT para autenticación, si no se especifica el tiempo de expiración se le
    # asigna un tiempo predeterminado.
    if expiration is None:
        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    data["exp"] = expiration
    token = jwt.encode(data, os.getenv("JWT_KEY"), algorithm="HS256")
    return token

def decode_token(token: str) -> dict | None:
    # Verifica el token JWT recibido por parte del cliente. Si éste ya expiró o es inválido,
    # se rechaza la autenticación.
    try:
        return jwt.decode(token, os.getenv("JWT_KEY"), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None