import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from sqlalchemy import create_engine
from .config import Config
from .webhooks.routes import webhook_bp
from .models.schema import Base

def create_app(config_class=Config):
    static_folder_path = os.path.join(os.path.dirname(__file__), 'static')
    app = Flask(__name__, static_folder=static_folder_path)
    app.config.from_object(config_class)
    
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Auto-initialize database tables
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(bind=engine)
    
    # Register blueprints
    app.register_blueprint(webhook_bp)

    @app.route("/", methods=["GET"])
    def index():
        return send_from_directory(static_folder_path, "index.html")

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return {
            "status": "online",
            "service": "Antigravity Automation Engine",
            "adapter_mode": Config.IG_DISPATCH_ADAPTER
        }, 200

    return app
