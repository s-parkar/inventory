from flask import Blueprint, jsonify, session
from app import supabase
import os

devops_bp = Blueprint('devops', __name__)

def get_user():
    token = session.get('access_token')
    if not token or not supabase:
        return None
    try:
        user = supabase.auth.get_user(token)
        return user
    except Exception as e:
        return None

@devops_bp.route('/health')
def health():
    """Simple Health Check"""
    app_version = os.getenv("APP_VERSION", "1.0.0")
    db_status = False
    if supabase:
        try:
            supabase.table('logs').select("count", count="exact").limit(1).execute()
            db_status = True
        except:
            db_status = False
            
    status = "healthy" if db_status else "degraded"
    return jsonify({
        "status": status,
        "db_connection": db_status,
        "version": app_version
    })

@devops_bp.route('/metrics')
def metrics():
    """Prometheus-style text metrics"""
    app_version = os.getenv("APP_VERSION", "1.0.0")
    try:
        prod_count = supabase.table('products').select("count", count="exact", head=True).execute().count
        log_count = supabase.table('logs').select("count", count="exact", head=True).execute().count
    except:
        prod_count = -1
        log_count = -1
        
    metrics_data = f"""
# HELP app_version_info Application version
# TYPE app_version_info gauge
app_version_info{{version="{app_version}"}} 1

# HELP inventory_total_products Total number of products in db
# TYPE inventory_total_products gauge
inventory_total_products {prod_count}

# HELP inventory_total_logs Total number of activity logs
# TYPE inventory_total_logs gauge
inventory_total_logs {log_count}
    """
    return metrics_data, 200, {'Content-Type': 'text/plain; version=0.0.4'}

@devops_bp.route('/simulate_error')
def simulate_error():
    """Endpoint to intentionally crash/error for testing alerts"""
    if not get_user():
        return jsonify({"error": "Unauthorized"}), 401
    
    raise Exception("Simulated Critical Error for DevOps Testing!")
