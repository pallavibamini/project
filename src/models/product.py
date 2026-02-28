from extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    sku = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    inventory = db.relationship("Inventory", back_populates="product", uselist=False)

    def to_dict(self):
        return {
            "id": int(self.id),
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "sku": self.sku,
        }
