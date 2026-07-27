from backend.app import create_app
from backend.database import init_db
app = create_app('default')
print('App created, initializing DB...')
with app.app_context():
    init_db(app)
print('DB initialized')
