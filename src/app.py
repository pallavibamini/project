from flask import Flask, jsonify, request, send_file
from config import Config
from extensions import db, init_mongo, migrate
import os

try:
    from logger import setup_logging, get_logger
except ImportError:
    import logging
    def setup_logging(app=None):
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger()
    def get_logger(name):
        return logging.getLogger(name)

try:
    from auth import setup_jwt, create_access_token
except ImportError:
    def setup_jwt(app):
        return None
    def create_access_token(identity):
        return None

from routes.user_route import user_bp
from routes.product_route import product_bp
from routes.order_route import order_bp

# Import models to register them with SQLAlchemy
from models.user import User
from models.product import Product
from models.inventory import Inventory
from models.order import Order, OrderItem

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config.from_object(Config)

# Enable CORS for frontend
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Setup logging
logger = setup_logging(app)

db.init_app(app)

# Initialize migrations only when migrate is available
if migrate is not None:
    migrate.init_app(app, db)

# Initialize JWT
setup_jwt(app)

# Initialize / provide mongo DB instance (callable from routes)
mongo_db = init_mongo(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(product_bp, url_prefix="/products")
app.register_blueprint(order_bp, url_prefix="/orders")


@app.route("/")
def index():
    """Serve the frontend SPA."""
    return send_file(os.path.join(app.static_folder, "index.html"))


@app.route("/health")
def health():
    return {"status": "OK"}, 200


@app.route("/auth/login", methods=["POST"])
def login():
    """Login endpoint (placeholder for demo)."""
    try:
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")

        if not (email and password):
            return jsonify({"error": "email and password are required"}), 400

        # For demo: accept any email/password (in production, hash and verify password)
        token = create_access_token(identity=email)
        if token:
            logger.info(f"Login: user={email}")
            return jsonify({"access_token": token, "token_type": "Bearer"}), 200
        else:
            # JWT not available
            logger.warning("JWT not available, returning dummy token")
            return jsonify({"access_token": "dummy_token_install_flask_jwt", "token_type": "Bearer"}), 200

    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/test-db")
def test_db():
    # quick smoke: count users
    try:
        from models.user import User
        users = User.query.all()
        logger.info(f"DB test: {len(users)} users found")
        return jsonify({"count": len(users)})
    except Exception as e:
        logger.error(f"DB test failed: {e}")
        return jsonify({"error": "Database error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)