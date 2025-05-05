from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from app.routes import bp as routes_bp
import os


def create_app():
    app = Flask(__name__)
    CORS(app)

    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "postgres")
    db_port = os.getenv("DB_PORT", "5432")

    db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    app.db_engine = create_engine(db_url, future=True)

    app.register_blueprint(routes_bp)
    return app
