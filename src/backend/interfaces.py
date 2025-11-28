import bcrypt
import secrets, datetime
from flask import jsonify

def http_result(code: int, status: str, data: dict | None = None, message: str | None = None):
    result = {
        "code": code,
        "status": status
    }

    if data is not None: result["data"] = data
    if message is not None and message.strip() != "": result["message"] = message

    return jsonify(result), code

def gen_token() -> dict:
    token = secrets.token_hex()
    hash_token = bcrypt.hashpw(token.encode(), bcrypt.gensalt(14))
    creation_date = datetime.datetime.now().isoformat()
    expiration_date = datetime.datetime.now() + datetime.timedelta(minutes=5)

    return {
        "token": token,
        "hash_token": hash_token.decode(),
        "creation_date": creation_date,
        "expiration_date": expiration_date
    }

def get_token_user(hash_tokens: tuple, token: str) -> int | None:
    token = token.encode()
    
    for element in hash_tokens:
        if bcrypt.checkpw(token, element["token"].encode()): return element["usuario_id"]
    
    return None