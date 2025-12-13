import os, datetime
from db import Database
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from interfaces import http_result, gen_uuid, decode_token

products = Blueprint("products", __name__)

# Carpetas de los archivos estáticos.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, "static", "product_imgs")
PICS_FOLDER = os.path.join("/static", "product_imgs")

# Extensiones de archivo permitidas para las imágenes.
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

def allowed_file(filename):
    # Verifica la extensión del archivo.
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def verify_images(pictures: list) -> str | None:
    for file in pictures:
        if not allowed_file(file.filename):
            return "Se debe incluir al menos una imagen. Sólo se permiten archivos con extensiones `.jpg`, `.png` y `.webp`."
        
        file_length = file.seek(0, 2)
        file.seek(0, 0)
        # Límite de 2 MiB.
        if file_length > 2097152: 
            return f"La imagen es demasiado grande. {file_length/1048576:.2f} MiB > 2 MiB."

    return None

def auth_user(token: str) -> dict | None:
    # Autenticación específicamente para las operaciones CUD.
    db = Database()

    user = db.selectOne({
        "table": "usuarios",
        "columns": ["id", "tipo"],
        "conditions": [
            {
            "prefix": "WHERE",
            "operator": "=",
            "column": "username",
            "value": token["username"]
            }
        ]
    })

    db.disconnect()

    if not user or user["tipo"] != "admin": 
        return None

    return user

@products.route("/", methods=["GET"])
def get_products():
    # Despliega todos los productos disponibles.
    db = Database()

    products = db.selectAll({
        "table": "tarjetas_productos",
        "columns": ["*"]
    })

    db.disconnect()

    if not products:
        return http_result(404, message="No se encontraron productos.")

    return http_result(200, data=products)

@products.route("/<product_id>", methods=["GET"])
def get_product(product_id):
    # Despliega la información del producto seleccionado, junto con sus imágenes
    db = Database()

    product = db.selectOne({
        "table": "productos",
        "columns": ["nombre", "precio", "descripcion", "stock"],
        "conditions": [
            {
            "prefix": "WHERE",
            "operator": "=",
            "column": "id",
            "value": product_id
            }
        ]
    })

    if not product:
        db.disconnect()
        return http_result(404, message="No se encontró el producto seleccionado.")
    
    images = db.selectAll({
        "table": "imagenes",
        "columns": ["ruta"],
        "conditions": [
            {
            "prefix": "WHERE",
            "operator": "=",
            "column": "producto_id",
            "value": product_id
            }
        ]
    })

    db.disconnect()

    product["imagenes"] = []

    for element in images:
        product["imagenes"].append(element["ruta"])

    return http_result(200, data=product)

@products.route("/", methods=["POST"])
def create_product():
    # Crea un producto nuevo
    auth = request.authorization

    if not auth:
        return http_result(400, message="Se requiere especificar un token.")

    token_user = decode_token(auth.token)

    if not token_user:
        return http_result(404, message="Token inválido.")

    user = auth_user(token_user)

    if not user:
        return http_result(403, message="No tienes permiso para acceder a este recurso.")

    nombre = request.form.get("productName")
    descripcion = request.form.get("productDescription")
    precio = request.form.get("productPrice")
    stock = request.form.get("productStock")

    if "" in [nombre, descripcion, precio, stock]:
        return http_result(400, message="Debes llenar todos los campos.")

    imagenes: list = request.files.getlist("productPics")
    message: str | None = verify_images(imagenes)

    if message is not None:
        return http_result(400, message=message)

    db = Database()

    newId = db.insertOne({
        "table": "productos",
        "columns": ["autor_id", "nombre", "descripcion", "precio", "stock", "fecha_creacion", "eliminado"],
        "values": [user["id"], nombre, descripcion, precio, stock, datetime.datetime.now(), False]
    })

    for file in imagenes:
        # Guarda cada imagen en su ruta y la agrega a la base de datos.
        file_uuid: str = gen_uuid()
        # Nombre de archivo: <UUID>.ext
        filename = f"{file_uuid}.{file.filename.rsplit('.', 1)[1].lower()}"

        folderName: str = os.path.join(STATIC_FOLDER, str(newId))
        os.makedirs(folderName, exist_ok=True)
        file.save(os.path.join(folderName, filename))

        folderName = os.path.join(PICS_FOLDER, str(newId))

        db.insertOne({
            "table": "imagenes",
            "columns": ["producto_id", "ruta"],
            "values": [newId, os.path.join(folderName, filename)]
        })
    
    return http_result(201, message="Producto creado exitosamente.")