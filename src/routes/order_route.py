from flask import Blueprint, request, jsonify
from extensions import db, init_mongo
from models.order import Order, OrderItem
from models.product import Product

try:
    from logger import get_logger
except ImportError:
    def get_logger(name):
        import logging
        return logging.getLogger(name)

try:
    from schemas import OrderCreate, OrderResponse
    HAS_SCHEMAS = True
except ImportError:
    HAS_SCHEMAS = False

logger = get_logger(__name__)
order_bp = Blueprint("orders", __name__)


@order_bp.route("/", methods=["POST"])
def create_order():
    """Create a new order with validation."""
    try:
        data = request.get_json() or {}

        if HAS_SCHEMAS:
            try:
                order_data = OrderCreate(**data)
                user_id = order_data.user_id
                items = order_data.items
                status = order_data.status
            except Exception as e:
                logger.warning(f"Validation error: {e}")
                return jsonify({"error": str(e)}), 400
        else:
            user_id = data.get("user_id")
            items = data.get("items", [])
            status = data.get("status", "pending")
            if not user_id or not items:
                return jsonify({"error": "user_id and items are required"}), 400

        order = Order(user_id=user_id, status=status)
        db.session.add(order)

        total = 0
        for it in items:
            product_id = it.get("product_id") if not HAS_SCHEMAS else it.product_id
            qty = int(it.get("quantity", 1) if not HAS_SCHEMAS else it.quantity)
            product = Product.query.get_or_404(product_id)
            unit_price = float(product.price)
            total += unit_price * qty
            oi = OrderItem(order=order, product_id=product_id, quantity=qty, unit_price=unit_price)
            db.session.add(oi)

        order.total = total
        db.session.commit()

        # Log to MongoDB
        mongo = init_mongo()
        if mongo:
            mongo.activity.insert_one({
                "action": "create_order",
                "order_id": order.id,
                "user_id": user_id,
                "total": float(total),
                "timestamp": db.func.now()
            })

        logger.info(f"Order created: id={order.id}, user_id={user_id}, total={total}")
        return jsonify(order.to_dict()), 201

    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return jsonify({"error": "Internal server error"}), 500


@order_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """Retrieve an order by ID with items."""
    try:
        order = Order.query.get_or_404(order_id)
        logger.info(f"Order retrieved: id={order_id}")
        return jsonify(order.to_dict())
    except Exception as e:
        logger.error(f"Error retrieving order {order_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500