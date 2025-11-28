import dotenv, os, json
from flask import Flask
from routes.users import users
from routes.auth import auth
from routes.tokens import tokens
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(users, url_prefix="/api/users")
app.register_blueprint(tokens, url_prefix="/api/tokens")

if __name__ == "__main__":
    dotenv.load_dotenv()

    app.run(host="localhost", debug=True)