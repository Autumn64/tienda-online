import dotenv, os, json
from flask import Flask
from routes.users import users
from routes.auth import auth
from routes.tokens import tokens
from flask_cors import CORS

app = Flask(__name__)
# Configuración de CORS para evitar errores en el cliente.
CORS(app)

# Se registra cada endpoint con su respectiva ruta. Se utiliza `Blueprint` para insertar
# cada endpoint de manera fácil y segura, y de este modo no llenamos un mismo archivo
# con demasiado código.
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(users, url_prefix="/api/users")
app.register_blueprint(tokens, url_prefix="/api/tokens")

if __name__ == "__main__":
    dotenv.load_dotenv()

    app.run(host="localhost", debug=True)