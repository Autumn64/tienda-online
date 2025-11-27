from db import Database
from flask import Blueprint, jsonify

users = Blueprint("users", __name__)

@users.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    db = Database()
    query: str = "SELECT username, email, tipo, eliminado FROM usuarios WHERE id=%s"

    user = db.selectOne(query, [user_id])

    if not user:
        return jsonify({
            "code": 404,
            "status": "fail",
            "message": "El usuario no existe."
        }), 404
    
    return jsonify({
        "code": 200,
        "status": "success",
        "data": user
    }), 200
