import dotenv, os, json
from flask import Flask
from users import users
from user_login import user_login
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_login, url_prefix="/api/auth/login")
app.register_blueprint(users, url_prefix="/api/users")

if __name__ == "__main__":
    dotenv.load_dotenv()

    app.run(host="localhost", debug=True)