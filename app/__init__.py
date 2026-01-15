from flask import Flask
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Global Supabase Client
supabase: Client = None

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev_secret_key")
    
    # Initialize Supabase
    global supabase
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if url and key:
        supabase = create_client(url, key)
    else:
        print("Warning: Supabase credentials not found in env.")

    # Import and Register Blueprints
    # Imported here to avoid circular dependencies with 'supabase' client
    from .routes.auth import auth_bp
    from .routes.inventory import inventory_bp
    from .routes.devops import devops_bp
    from .routes.admin import admin_bp
    from .routes.supplier import supplier_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(devops_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(supplier_bp)

    return app
