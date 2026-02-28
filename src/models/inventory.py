from extensions import db


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.BigInteger, primary_key=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey("products.id"), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    location = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    product = db.relationship("Product", back_populates="inventory", uselist=False)

    def to_dict(self):
        return {"id": int(self.id), "product_id": int(self.product_id), "quantity": self.quantity, "location": self.location}
