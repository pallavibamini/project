"""Alembic script template"""

# Auto-generated migration: initial schema
# This migration creates the initial database tables

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'initial_001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create initial schema with all tables."""
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    # Create products table
    op.create_table(
        'products',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('sku', sa.String(100), unique=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    # Create orders table
    op.create_table(
        'orders',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BigInteger, nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('total', sa.Numeric(12, 2), server_default='0.00'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )

    # Create order_items table
    op.create_table(
        'order_items',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('order_id', sa.BigInteger, nullable=False),
        sa.Column('product_id', sa.BigInteger, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False, server_default='1'),
        sa.Column('unit_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='RESTRICT')
    )

    # Create inventory table
    op.create_table(
        'inventory',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('product_id', sa.BigInteger, nullable=False, unique=True),
        sa.Column('quantity', sa.Integer, nullable=False, server_default='0'),
        sa.Column('location', sa.String(255)),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE')
    )


def downgrade():
    """Drop all tables."""
    op.drop_table('inventory')
    op.drop_table('order_items')
    op.drop_table('orders')
    op.drop_table('products')
    op.drop_table('users')
