from db import Database
from flask import Blueprint, jsonify

users = Blueprint("users", __name__)

@users.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    db = Database()

    user = db.selectOne({
        "table": "usuarios",
        "columns": ["username", "email", "tipo", "eliminado"],
        "condition": {
            "operator": "=",
            "column": "id",
            "value": user_id
        }
    })

    db.disconnect()

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
