# app/__init__.py

import os
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from dotenv import load_dotenv
import time
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

    db_url = os.environ.get('DATABASE_URL')

    if not db_url:
        logger.error("💥💥💥 FATAL ERROR: DATABASE_URL environment variable is NOT set! 💥💥💥")
        logger.error("The app cannot run without a database. Check Bitbucket/Cloud Run variables.")
        raise ValueError("DATABASE_URL is required. Cannot fallback to SQLite.")

        # ... previous code ...
    
    logger.info(f"📡 Connecting to Neon Database: {db_url[:30]}...")
    if 'postgres' in db_url:
        if 'sslmode' not in db_url:
            sep = '&' if '?' in db_url else '?'
            db_url += f"{sep}sslmode=require"
            logger.info("✅ Added sslmode=require to URL")
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
            logger.info("✅ Fixed protocol to postgresql://")

    # ✅ FIX THIS LINE BELOW:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url  # Changed from 'DATABASE_URI'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'connect_args': {'connect_timeout': 10}
    }

    try:
        db.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = 'main.login'
        socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')
        logger.info("✅ Extensions initialized.")
    except Exception as e:
        logger.error(f"💥 Failed to initialize extensions: {e}")
        raise e

    with app.app_context():
        try:
            logger.info("🔍 Attempting database connection...")
            start_time = time.time()
            with db.engine.connect() as conn:
                conn.execute(db.text("SELECT 1"))
            elapsed = time.time() - start_time
            logger.info(f"✅ Database connected successfully in {elapsed:.2f}s")

            logger.info("🏗️ Creating/Verifying tables...")
            db.create_all()
            logger.info("✅ Tables verified/created.")

            from app.models import User # This import is now safe
            if not User.query.filter_by(username='admin').first():
                logger.info("👤 Creating default admin user...")
                admin = User(username='admin', email='admin@ampoulex.com', role='admin', is_active=True)
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                logger.info("✅ Admin user created (admin/admin123).")
            else:
                logger.info("✅ Admin user already exists.")
        except Exception as e:
            logger.error(f"💥💥💥 DATABASE CONNECTION FAILED 💥💥💥")
            logger.error(f"Error Type: {type(e).__name__}")
            logger.error(f"Error Message: {str(e)}")
            logger.error("Check your DATABASE_URL variable in Bitbucket/Cloud Run.")
            logger.error("Ensure it ends with ?sslmode=require and has no channel_binding.")
            raise e

    # --- IMPORTANT CHANGE HERE ---
    # Move the import and registration of blueprints AFTER extensions are initialized
    try:
        logger.info("🗺️ Registering routes...")
        from app.routes import main_bp # This import is now safe
        app.register_blueprint(main_bp)
        logger.info("✅ Routes registered successfully.")
    except Exception as e:
        logger.error(f"💥💥💥 FAILED TO REGISTER ROUTES 💥💥💥")
        logger.error(f"Error Type: {type(e).__name__}")
        logger.error(f"Error Message: {str(e)}")
        logger.error("Likely cause: Missing file (e.g., app/utils/tax_calculator.py) or Syntax Error in routes.py")
        raise e

    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "message": "App is running on Neon DB"}), 200

    return app