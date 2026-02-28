from flask import Blueprint, request, jsonify
from extensions import db, init_mongo
from models.user import User

try:
    from logger import get_logger
except ImportError:
    def get_logger(name):
        import logging
        return logging.getLogger(name)

try:
    from schemas import UserCreate, UserUpdate, UserResponse
    HAS_SCHEMAS = True
except ImportError:
    HAS_SCHEMAS = False

logger = get_logger(__name__)
user_bp = Blueprint("users", __name__)


@user_bp.route("/", methods=["POST"])
def create_user():
    """Create a new user with validation."""
    try:
        data = request.get_json() or {}

        # Validate request data
        if HAS_SCHEMAS:
            try:
                user_data = UserCreate(**data)
                name = user_data.name
                email = user_data.email
                password = user_data.password
            except Exception as e:
                logger.warning(f"Validation error: {e}")
                return jsonify({"error": str(e)}), 400
        else:
            # Fallback validation
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            if not (name and email and password):
                return jsonify({"error": "name, email and password are required"}), 400

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            logger.warning(f"User creation failed: email {email} already exists")
            return jsonify({"error": "Email already exists"}), 409

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        # Log creation to MongoDB
        mongo = init_mongo()
        if mongo:
            mongo.activity.insert_one({
                "action": "create_user",
                "user_id": user.id,
                "email": email,
                "timestamp": db.func.now()
            })

        logger.info(f"User created: id={user.id}, email={email}")
        return jsonify({"id": user.id, "name": user.name, "email": user.email}), 201

    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return jsonify({"error": "Internal server error"}), 500


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Retrieve a user by ID."""
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "name": user.name, "email": user.email})


@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Update a user with validation."""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json() or {}

        if HAS_SCHEMAS:
            try:
                user_data = UserUpdate(**data)
                if user_data.name:
                    user.name = user_data.name
                if user_data.email:
                    user.email = user_data.email
            except Exception as e:
                logger.warning(f"Validation error: {e}")
                return jsonify({"error": str(e)}), 400
        else:
            if "name" in data:
                user.name = data["name"]
            if "email" in data:
                user.email = data["email"]

        db.session.commit()
        logger.info(f"User updated: id={user_id}")
        return jsonify({"id": user.id, "name": user.name, "email": user.email})

    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user."""
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        logger.info(f"User deleted: id={user_id}")
        return jsonify({"deleted": True}), 200
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500