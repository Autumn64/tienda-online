from flask import jsonify

def http_result(code: int, status: str, data: dict | None = None, message: str | None = None):
    result = {
        "code": code,
        "status": status
    }

    if data is not None: result["data"] = data
    if message is not None and message.strip() != "": result["message"] = message

    return jsonify(result), code