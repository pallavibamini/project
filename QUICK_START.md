# 🚀 QUICK START GUIDE - Copy & Paste Commands

## Start Your System (Choose One Method)

### **Method 1: Fastest - Run Start Script** ⚡
```bash
cd /Users/baminipallavi/Desktop/test_folder
./start.sh
```

### **Method 2: Manual Start** 
```bash
cd /Users/baminipallavi/Desktop/test_folder
source .venv/bin/activate
cd src
python3 -m flask run --host=0.0.0.0 --port=5001
```

### **Method 3: Using Docker** 🐳
```bash
cd /Users/baminipallavi/Desktop/test_folder
docker-compose -f docker/docker-compose.yml up -d
```

---

## 🌐 Once Running

### Open Frontend
```
http://localhost:5001
```

### Login Credentials
```
Email: 238r1a0465@gmail.com
Password: any password
```

---

## 📡 Test API Endpoints

### Get JWT Token
```bash
curl -X POST http://localhost:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"238r1a0465@gmail.com","password":"password"}'
```

### List Products
```bash
curl 'http://localhost:5001/products/?page=1&per_page=10'
```

### List Users
```bash
curl 'http://localhost:5001/users/?page=1&per_page=10'
```

### Create Product
```bash
curl -X POST http://localhost:5001/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "description": "A test product",
    "price": 99.99,
    "sku": "TEST-001"
  }'
```

### Create User
```bash
curl -X POST http://localhost:5001/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Health Check
```bash
curl http://localhost:5001/health
```

---

## 🔧 Useful Commands

### Check if MySQL is running
```bash
mysql -u root -p'pallavi@2004' -e "SELECT 1"
```

### Check if MongoDB is running
```bash
mongosh localhost:27017
```

### Stop Flask server
```
Press Ctrl+C in the terminal
```

### Kill process on port 5001 (if stuck)
```bash
lsof -i :5001 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### View MySQL database
```bash
mysql -u root -p'pallavi@2004'
USE inventory_db;
SHOW TABLES;
SELECT COUNT(*) FROM products;
```

### View MongoDB logs
```bash
mongosh localhost:27017/logs_db
db.activity.find().limit(5)
```

---

## 📊 Database Credentials

```
MySQL:
- Host: localhost
- Port: 3306
- User: root
- Password: pallavi@2004
- Database: inventory_db

MongoDB:
- Host: localhost
- Port: 27017
- Database: logs_db
```

---

## 🐛 If Something Goes Wrong

### Flask app won't start
1. Check if port 5001 is in use: `lsof -i :5001`
2. Kill it if needed: `lsof -i :5001 | grep LISTEN | awk '{print $2}' | xargs kill -9`
3. Restart Flask

### Can't connect to MySQL
1. Check MySQL is running: `mysql -u root -p'pallavi@2004' -e "SELECT 1"`
2. Verify credentials in `.env`
3. Check port 3306 is not in use: `lsof -i :3306`

### Can't connect to MongoDB
- MongoDB is optional - app works without it
- Check if running: `mongosh localhost:27017`
- Activity logging will be skipped

### Virtual environment issues
```bash
cd /Users/baminipallavi/Desktop/test_folder
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🎯 Common Tasks

### View all products in database
```bash
mysql -u root -p'pallavi@2004' -e "USE inventory_db; SELECT id, name, price FROM products;"
```

### Delete all products
```bash
mysql -u root -p'pallavi@2004' -e "USE inventory_db; DELETE FROM products; DELETE FROM inventory;"
```

### Reset database (careful!)
```bash
mysql -u root -p'pallavi@2004' -e "DROP DATABASE inventory_db; CREATE DATABASE inventory_db;"
mysql -u root -p'pallavi@2004' inventory_db < /Users/baminipallavi/Desktop/test_folder/db/schema.sql
mysql -u root -p'pallavi@2004' inventory_db < /Users/baminipallavi/Desktop/test_folder/db/seed.sql
```

### View application logs
```bash
# Check the terminal where Flask is running
# Or tail the log file if configured
tail -f /path/to/app.log
```

---

## ✨ Pro Tips

- **Frontend Changes**: Just refresh the browser (http://localhost:5001)
- **Backend Changes**: Flask auto-reloads when you save files
- **Add Dependencies**: Edit requirements.txt and reinstall:
  ```bash
  pip install -r requirements.txt
  ```
- **Debug Mode**: Already enabled - server restarts on errors
- **CORS**: All endpoints allow cross-origin requests

---

## 📚 File Reference

```
/Users/baminipallavi/Desktop/test_folder/
├── start.sh                    # Quick start script ← USE THIS
├── .env                        # Environment config
├── requirements.txt            # Python packages
├── README.md                   # Full documentation
├── SETUP_COMPLETE.md           # Setup status
├── QUICK_START.md              # This file
├── src/
│   ├── app.py                 # Flask entry point
│   ├── config.py              # Database config
│   └── static/index.html      # Frontend SPA
├── db/
│   ├── schema.sql             # Database schema
│   └── seed.sql               # Sample data
└── docker/
    └── docker-compose.yml     # Docker setup
```

---

## 🚀 You're Ready!

### To Start Now:
```bash
cd /Users/baminipallavi/Desktop/test_folder && ./start.sh
```

### Then Open:
```
http://localhost:5001
```

### Login With:
```
Email: 238r1a0465@gmail.com
Password: any password
```

---

**That's it! Your system is ready to use.** 🎉

For more detailed info, see `SETUP_COMPLETE.md` or `README.md`
