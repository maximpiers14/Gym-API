from flask import Flask
from api_routes import api
from web_routes import web
from database import init_db

app = Flask(__name__)

app.secret_key = "secret"
app.config.update({
    "SESSION_COOKIE_SAMESITE": "Lax",
    "SESSION_COOKIE_HTTPONLY": True
})

app.register_blueprint(api)
app.register_blueprint(web)

init_db()

if __name__ == "__main__":
    app.run(debug=True) # delete debug mode later