# Cloud-Native Inventory & Order Management System

A modern, containerized Flask backend for inventory and order management with full REST API support, MongoDB logging, and JWT authentication.

## Features

- **Users, Products, Orders, Inventory** — Full CRUD operations via REST API
- **SQL (MySQL)** persistence with SQLAlchemy ORM
- **MongoDB** activity/event logging
- **JWT Authentication** with Flask-JWT-Extended
- **Input Validation** with Pydantic schemas
- **Structured Logging** with python-json-logger
- **Dockerized services** (app, MySQL, MongoDB) via docker-compose
- **Database Migrations** with Flask-Migrate/Alembic
- **GitHub Actions CI/CD** with integration tests
- **Interactive Frontend** (HTML/CSS/vanilla JS SPA)

## Project Structure

```
├── src/
│   ├── app.py              # Main Flask app
│   ├── config.py           # Configuration
│   ├── extensions.py       # SQLAlchemy, Migrate
│   ├── auth.py             # JWT utilities
│   ├── logger.py           # Structured logging
│   ├── schemas.py          # Pydantic request validation
│   ├── models/             # ORM models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── inventory.py
│   ├── routes/             # API blueprints
│   │   ├── user_route.py
│   │   ├── product_route.py
│   │   └── order_route.py
│   └── static/
│       └── index.html      # Frontend SPA
├── db/
│   ├── schema.sql          # MySQL schema
│   └── seed.sql            # Initial data
├── docker/
│   ├── Dockerfile          # Backend image
│   └── docker-compose.yml  # Services
├── migrations/             # Alembic migrations
├── tests/                  # Unit/integration tests
├── .github/workflows/      # CI/CD
└── requirements.txt        # Dependencies

```

## Quick Start

### Prerequisites
- Docker & Docker Compose (or local MySQL + MongoDB)
- Python 3.11+

### 1. Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start Services

```bash
cp .env.example .env
docker compose -f docker/docker-compose.yml up --build -d
```

Or without Docker:
```bash
# Install MySQL and MongoDB locally, then
export DB_HOST=localhost MONGO_HOST=localhost
python3 src/app.py
```

### 3. Access the App

- **Frontend SPA**: http://localhost:5001
- **API Health**: http://localhost:5001/health
- **DB Test**: http://localhost:5001/test-db

## API Endpoints

### Users
- `POST /users/` — Create user
- `GET /users/<id>` — Get user
- `PUT /users/<id>` — Update user
- `DELETE /users/<id>` — Delete user

### Products
- `POST /products/` — Create product
- `GET /products/` — List products (paginated)
- `PUT /products/<id>` — Update product
- `DELETE /products/<id>` — Delete product

### Orders
- `POST /orders/` — Create order
- `GET /orders/<id>` — Get order with items

### Auth
- `POST /auth/login` — Login (returns JWT token)

### Health
- `GET /health` — Health check
- `GET /test-db` — DB connectivity test

## Request/Response Examples

### Create User
```bash
curl -X POST http://localhost:5001/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com", "password": "secret123"}'
```

### Create Product
```bash
curl -X POST http://localhost:5001/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget", "price": 9.99, "sku": "WGT-001"}'
```

### Create Order
```bash
curl -X POST http://localhost:5001/orders/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "items": [{"product_id": 1, "quantity": 2}]}'
```

### Login & Get Token
```bash
curl -X POST http://localhost:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "secret123"}'
```

## Database Migrations (Flask-Migrate)

Initialize migrations (first time only):
```bash
export FLASK_APP=src.app
flask db init
```

Create a migration after model changes:
```bash
flask db migrate -m "describe your changes"
```

Apply migrations:
```bash
flask db upgrade
```

Or use the Makefile shortcuts:
```bash
make migrate-init
make migrate-make MIGRATION_MESSAGE="your message"
make migrate
```

## Input Validation

All endpoints use Pydantic schemas for request validation:
- Email validation with `EmailStr`
- Required fields and field length constraints
- Price and quantity validation
- Detailed error messages on validation failure

Example error response:
```json
{"error": "1 validation error for UserCreate..."}
```

## Authentication & Authorization

JWT tokens are generated on login and can be included in subsequent requests:
```bash
Authorization: Bearer <your_token>
```

Currently, the `/auth/login` endpoint accepts any email/password. In production:
- Hash passwords with bcrypt/argon2
- Validate credentials against DB
- Set token expiry and refresh token strategy

## Logging

Structured logging to stdout (JSON format when `python-json-logger` is available):
- User creation, updates, deletions
- Product operations
- Order creation with total amount
- Login events
- Errors with stack traces

Log format: `{"timestamp": "...", "level": "INFO", "name": "...", "message": "..."}`

## Activity Logging (MongoDB)

Create, update, and login events are logged to MongoDB collection `activity`:
```json
{
  "action": "create_user",
  "user_id": 1,
  "email": "john@example.com",
  "timestamp": "2026-02-28T12:00:00"
}
```

## Testing

Run unit tests:
```bash
python3 -m pytest -q
```

Current test coverage:
- User creation with in-memory SQLite DB
- Blueprint registration
- Basic endpoint functionality

Integration tests (SQL + MongoDB) coming soon.

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`):
- Runs on push/PR to `main`
- Spins up MySQL and MongoDB services
- Installs dependencies
- Runs pytest suite
- Validates no breaking changes

## Troubleshooting

### Docker daemon not running
```bash
open -a Docker  # macOS
# or use Colima instead
brew install colima
colima start
```

### Flask-Migrate issues
Ensure `FLASK_APP=src.app` is set and dependencies are installed:
```bash
pip install Flask-Migrate
```

### Database connection errors
Check `.env` settings match your DB credentials:
```bash
cat .env
# Adjust as needed
```

### Port conflicts
If 5001, 3306, or 27017 are in use, update `.env` or docker-compose.yml:
```yaml
ports:
  - "5002:5001"  # app on 5002
```

## Production Considerations

- [ ] Use environment variables for secrets (not `.env` files)
- [ ] Enable HTTPS/TLS
- [ ] Add request rate limiting and throttling
- [ ] Implement proper password hashing (bcrypt)
- [ ] Use a production WSGI server (gunicorn, uwsgi)
- [ ] Add database connection pooling
- [ ] Set up monitoring and alerting (logs, metrics)
- [ ] Add request/response logging middleware
- [ ] Implement proper error handling and reporting
- [ ] Use a secrets management system (AWS Secrets Manager, Vault)

## Next Steps

- [ ] Add email verification for user signup
- [ ] Implement inventory stock management
- [ ] Add order status workflow (pending → processing → shipped → delivered)
- [ ] Build customer dashboard frontend
- [ ] Add analytics API (sales, inventory trends)
- [ ] Set up multi-tenant support
- [ ] Add API rate limiting
- [ ] Create mobile app (React Native/Flutter)

## License

MIT License. See LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

