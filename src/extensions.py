from flask_sqlalchemy import SQLAlchemy
import os

# Attempt to optionally import Flask-Migrate; don't raise at import time if it's missing.
try:
	from flask_migrate import Migrate
except Exception:
	Migrate = None

db = SQLAlchemy()
# Create migrate only if the package is available; caller should check before using.
migrate = Migrate() if Migrate is not None else None


def init_mongo(app=None):
	"""Initialize and return a PyMongo database instance, or None on failure.

	This function imports pymongo lazily so the package is optional at import-time.
	"""
	try:
		from pymongo import MongoClient
	except Exception:
		return None

	mongo_host = os.environ.get("MONGO_HOST", "localhost")
	mongo_port = int(os.environ.get("MONGO_PORT", 27017))
	mongo_db_name = os.environ.get("MONGO_DB", "logs_db")

	try:
		client = MongoClient(host=mongo_host, port=mongo_port)
		db_inst = client[mongo_db_name]
		return db_inst
	except Exception:
		return None