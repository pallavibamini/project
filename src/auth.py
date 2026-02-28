"""JWT authentication utilities using Flask-JWT-Extended."""

from datetime import timedelta
import os


def setup_jwt(app):
    """Configure JWT for the Flask app."""
    try:
        from flask_jwt_extended import JWTManager
    except ImportError:
        return None

    # Configure JWT
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-in-prod")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    jwt = JWTManager(app)
    return jwt


def create_access_token(identity):
    """Create a JWT access token for the given identity."""
    try:
        from flask_jwt_extended import create_access_token as jwt_create_access_token
    except ImportError:
        return None
    return jwt_create_access_token(identity=identity)


def get_jwt_identity():
    """Get the identity from the current JWT token."""
    try:
        from flask_jwt_extended import get_jwt_identity as jwt_get_identity
    except ImportError:
        return None
    return jwt_get_identity()
