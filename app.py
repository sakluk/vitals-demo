"""
app.py — VitalsDemo Flask-sovelluksen pääohjelma.

Käyttö:
    pip install -r requirements.txt
    python init_db.py
    python app.py
"""

import os

from flask import Flask

import models
from auth import auth_bp, login_manager
from routes import main_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    app.config["DATABASE"] = os.path.join(BASE_DIR, "vitals.db")

    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    app.teardown_appcontext(models.close_db)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
