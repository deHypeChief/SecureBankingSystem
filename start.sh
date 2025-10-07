#!/bin/bash

# Production startup script for Secure Banking System

# Set default values
export FLASK_ENV=${FLASK_ENV:-production}
export PORT=${PORT:-5000}
export SECRET_KEY=${SECRET_KEY:-$(python -c "import secrets; print(secrets.token_hex(32))")}

echo "🚀 Starting Secure Banking System..."
echo "🌐 Environment: $FLASK_ENV"
echo "🔌 Port: $PORT"
echo "🔐 Secret key configured"

# Run with gunicorn for production
if [ "$FLASK_ENV" = "production" ]; then
    echo "📦 Starting with Gunicorn (Production Mode)"
    exec gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 30 --keep-alive 2 --max-requests 1000 --max-requests-jitter 50 web_app:app
else
    echo "🔧 Starting with Flask Development Server"
    exec python web_app.py
fi