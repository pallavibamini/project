USE inventory_db;

INSERT INTO users (name, email, password) VALUES
('Alice', 'alice@example.com', 'password1'),
('Bob', 'bob@example.com', 'password2');

INSERT INTO products (name, description, price, sku) VALUES
('Widget', 'A useful widget', 9.99, 'WGT-001'),
('Gadget', 'A handy gadget', 19.99, 'GDT-001');

INSERT INTO inventory (product_id, quantity, location) VALUES
(1, 100, 'warehouse-a'),
(2, 50, 'warehouse-b');
