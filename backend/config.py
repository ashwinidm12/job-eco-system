"""
Application configuration for Job Eco System backend.
Uses environment variables with safe defaults for development.
Loads .env from backend directory if present (so MONGODB_URI works without exporting).
"""
import os

# Load .env file so MONGODB_URI and JWT_SECRET can be set there
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass  # dotenv optional; use env vars or defaults


class Settings:
    """App settings from environment or defaults."""

    # MongoDB connection string (required in production)
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

    # JWT: secret key for signing tokens. MUST be set in production.
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret-change-in-production")

    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days


settings = Settings()
