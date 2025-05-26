# Configuration settings

import os

class Config:
    """Base configuration class."""
    PROJECT_NAME = "CogniForm"
    VERSION = "0.1.0"
    DESCRIPTION = "An interactive cognitive science survey platform."
    
    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
    
    # FastAPI settings
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "t")
    
    # CORS settings
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")