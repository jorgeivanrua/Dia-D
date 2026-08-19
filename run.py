# run.py - Module-level app for gunicorn 'run:app'
from backend.app import create_app

app = create_app()