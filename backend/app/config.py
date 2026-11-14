import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "antigravity-dev-secret-key-32b")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///antigravity.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Celery & Redis
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
    
    # Instagram Graph API & Webhook Secret
    INSTAGRAM_APP_SECRET = os.getenv("INSTAGRAM_APP_SECRET", "meta_app_secret_placeholder")
    INSTAGRAM_VERIFY_TOKEN = os.getenv("INSTAGRAM_VERIFY_TOKEN", "antigravity_webhook_verify_token")
    INSTAGRAM_GRAPH_API_VERSION = os.getenv("INSTAGRAM_GRAPH_API_VERSION", "v19.0")
    
    # Message Dispatcher Mode: 'graph_api' or 'instagrapi'
    IG_DISPATCH_ADAPTER = os.getenv("IG_DISPATCH_ADAPTER", "instagrapi")
    INSTAGRAPI_SESSION_CACHE = os.getenv("INSTAGRAPI_SESSION_CACHE", "instagrapi_session.json")
    
    # AI Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Referral Tracking
    BASE_TRACKING_URL = os.getenv("BASE_TRACKING_URL", "https://antigrav.link/r/")
