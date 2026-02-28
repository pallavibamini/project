import pytest

from flask import Flask

import sys
# Make src/ importable as top-level package root for test imports that mirror runtime
sys.path.insert(0, './src')

from extensions import db


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # import models to create tables
        from models.user import User
        from models.product import Product
        from models.order import Order, OrderItem
        db.create_all()
        # register routes blueprints used by tests (import using runtime-style imports)
        from routes.user_route import user_bp
        app.register_blueprint(user_bp, url_prefix="/users")
        yield app


def test_create_user(app):
    client = app.test_client()
    res = client.post('/users/', json={"name": "Test", "email": "t@example.com", "password": "p"})
    assert res.status_code == 201
    data = res.get_json()
    assert data['email'] == 't@example.com'
