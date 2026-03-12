import sys
import os

# Add the project root to the path so app_auth can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_auth import app, db

# Vercel expects a WSGI callable named `app`
with app.app_context():
    db.create_all()  # Auto-create tables on first cold start
