import dotenv, os, json
from flask_cors import CORS
from routes.auth import auth
from routes.users import users
from routes.tokens import tokens
from routes.checkout import checkout
from routes.products import products
from werkzeug.utils import safe_join
from flask import Flask, send_from_directory, abort

# Carpetas de la app y de los archivos estáticos.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, "static")

app = Flask(__name__)
# Configuración de CORS para evitar errores en el cliente.
CORS(app)

# Se registra cada endpoint con su respectiva ruta. Se utiliza `Blueprint` para insertar
# cada endpoint de manera fácil y segura, y de este modo no llenamos un mismo archivo
# con demasiado código.
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(users, url_prefix="/api/users")
app.register_blueprint(tokens, url_prefix="/api/tokens")
app.register_blueprint(checkout, url_prefix="/api/checkout")
app.register_blueprint(products, url_prefix="/api/products")

@app.route("/static/<path:subpath>")
def serveStatic(subpath):
    # Sirve archivos estáticos (como imágenes) de la carpeta `/static`.
    safePath = safe_join(STATIC_FOLDER, subpath)
    if not safePath or not os.path.isfile(safePath): abort(404)

    folder = os.path.dirname(safePath)
    filename = os.path.basename(safePath)

    return send_from_directory(folder, filename)

if __name__ == "__main__":
    dotenv.load_dotenv()

    app.run(host="localhost", debug=True)