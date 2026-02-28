from extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")
    total = db.Column(db.Numeric(12, 2), default=0.00)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": int(self.id),
            "user_id": int(self.user_id),
            "status": self.status,
            "total": float(self.total),
            "items": [i.to_dict() for i in self.items],
        }


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.BigInteger, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    order = db.relationship("Order", back_populates="items")

    def to_dict(self):
        return {
            "id": int(self.id),
            "order_id": int(self.order_id),
            "product_id": int(self.product_id),
            "quantity": self.quantity,
            "unit_price": float(self.unit_price),
        }
