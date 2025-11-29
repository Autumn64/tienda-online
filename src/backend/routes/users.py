from db import Database
from interfaces import http_result
from flask import Blueprint, jsonify

users = Blueprint("users", __name__)

@users.route("/<user_id>", methods=["GET"])
# La ruta de este endpoint sería /api/users/<id_del_usuario>
def get_user(user_id):
    db = Database()

    user = db.selectOne({
        "table": "usuarios",
        "columns": ["username", "email", "tipo", "eliminado"],
        "conditions": [
            {
            "prefix": "WHERE",
            "operator": "=",
            "column": "id",
            "value": user_id
            }
        ]
    })

    db.disconnect()

    if not user:
        return http_result(404, message="El usuario no existe.")
    
    return http_result(404, data=user)
