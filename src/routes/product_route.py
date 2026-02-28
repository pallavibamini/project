from flask import Blueprint, request, jsonify
from extensions import db, init_mongo
from models.product import Product

try:
    from logger import get_logger
except ImportError:
    def get_logger(name):
        import logging
        return logging.getLogger(name)

try:
    from schemas import ProductCreate, ProductUpdate, ProductResponse
    HAS_SCHEMAS = True
except ImportError:
    HAS_SCHEMAS = False

logger = get_logger(__name__)
product_bp = Blueprint("products", __name__)


@product_bp.route("/", methods=["POST"])
def create_product():
    """Create a new product with validation."""
    try:
        data = request.get_json() or {}

        if HAS_SCHEMAS:
            try:
                prod_data = ProductCreate(**data)
                name = prod_data.name
                description = prod_data.description
                price = prod_data.price
                sku = prod_data.sku
            except Exception as e:
                logger.warning(f"Validation error: {e}")
                return jsonify({"error": str(e)}), 400
        else:
            name = data.get("name")
            price = data.get("price")
            if not (name and price is not None):
                return jsonify({"error": "name and price are required"}), 400
            description = data.get("description")
            sku = data.get("sku")

        product = Product(name=name, description=description, price=price, sku=sku)
        db.session.add(product)
        db.session.commit()

        # Log to MongoDB
        mongo = init_mongo()
        if mongo:
            mongo.activity.insert_one({
                "action": "create_product",
                "product_id": product.id,
                "name": name,
                "timestamp": db.func.now()
            })

        logger.info(f"Product created: id={product.id}, name={name}")
        return jsonify(product.to_dict()), 201

    except Exception as e:
        logger.error(f"Error creating product: {e}")
        return jsonify({"error": "Internal server error"}), 500


@product_bp.route("/", methods=["GET"])
def list_products():
    """List products with pagination."""
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
        q = Product.query.paginate(page=page, per_page=per_page, error_out=False)
        items = [p.to_dict() for p in q.items]
        logger.info(f"Listed products: page={page}, count={len(items)}")
        return jsonify({"items": items, "total": q.total})
    except Exception as e:
        logger.error(f"Error listing products: {e}")
        return jsonify({"error": "Internal server error"}), 500


@product_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Update a product with validation."""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json() or {}

        if HAS_SCHEMAS:
            try:
                prod_data = ProductUpdate(**data)
                if prod_data.price is not None:
                    product.price = prod_data.price
                if prod_data.name:
                    product.name = prod_data.name
                if prod_data.description:
                    product.description = prod_data.description
            except Exception as e:
                logger.warning(f"Validation error: {e}")
                return jsonify({"error": str(e)}), 400
        else:
            if "price" in data:
                product.price = data["price"]
            if "name" in data:
                product.name = data["name"]

        db.session.commit()
        logger.info(f"Product updated: id={product_id}")
        return jsonify(product.to_dict())

    except Exception as e:
        logger.error(f"Error updating product {product_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500


@product_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a product."""
    try:
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        logger.info(f"Product deleted: id={product_id}")
        return jsonify({"deleted": True}), 200
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500