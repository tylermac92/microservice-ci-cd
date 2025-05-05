from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from app.routes import bp as routes_bp
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    db_url = os.getenv("DATABASE_URL")
    app.db_engine = create_engine(db_url, future=True)

    app.register_blueprint(routes_bp)
    return app
