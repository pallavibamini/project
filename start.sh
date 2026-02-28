#!/bin/bash

# Quick Start Script for Inventory Management System

echo "🚀 Starting Inventory Management System..."
echo ""

# Check if in correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the test_folder directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source .venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check MySQL connection
echo "🔍 Checking MySQL connection..."
mysql -u root -p'pallavi@2004' -e "SELECT 1" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Cannot connect to MySQL"
    echo "   Make sure MySQL is running with your credentials"
fi

# Check MongoDB connection (optional)
echo "🔍 Checking MongoDB connection..."
# Just try to connect without failing if not available
echo "db.version()" | mongosh localhost:27017 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ MongoDB is connected"
else
    echo "⚠️  MongoDB not available (optional - activity logging will be skipped)"
fi

# Start Flask app
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Starting Flask Application..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Frontend: http://localhost:5001"
echo "📚 API Root: http://localhost:5001/api"
echo "🛑 Press Ctrl+C to stop the server"
echo ""
echo "Test Credentials:"
echo "  Email: 238r1a0465@gmail.com"
echo "  Email: user2@example.com"
echo "  Password: any password works"
echo ""

# Change to src directory and run Flask
cd src
python3 -m flask run --host=0.0.0.0 --port=5001 --reload
