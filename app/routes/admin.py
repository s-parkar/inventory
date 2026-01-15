from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app import supabase
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def is_admin():
    role = session.get('role')
    return role == 'admin'

@admin_bp.before_request
def check_admin():
    if not session.get('access_token'):
        return redirect(url_for('auth.login'))
    if not is_admin():
        flash("Access Denied: Admin only.", "error")
        return redirect(url_for('inventory.dashboard')) # Fallback

@admin_bp.route('/dashboard')
def dashboard():
    app_version = os.getenv("APP_VERSION", "1.0.0")
    
    # Fetch All Users (using a view or direct rpc if setup, for now mock or simple select if RLS allows)
    # Note: supabase-py client doesn't give easy list_users without service key. 
    # For this demo, we'll query user_roles to list "users"
    try:
        users_res = supabase.table('user_roles').select('*').execute()
        users = users_res.data
    except:
        users = []

    # Fetch All Logs
    try:
        logs_res = supabase.table('logs').select("*").order('timestamp', desc=True).limit(50).execute()
        logs = logs_res.data
    except:
        logs = []

    # Fetch All Products
    try:
        products_res = supabase.table('products').select("*").order('created_at', desc=True).execute()
        products = products_res.data
    except:
        products = []

    return render_template('admin_dashboard.html', users=users, logs=logs, products=products, version=app_version, user=session.get('role'))

@admin_bp.route('/delete_product/<product_id>', methods=['POST'])
def delete_product(product_id):
    try:
        supabase.table('products').delete().eq('id', product_id).execute()
        
        # Log action
        log_data = {"action": f"Admin deleted product {product_id}"}
        supabase.table('logs').insert(log_data).execute()
        
        flash("Product deleted.", "success")
    except Exception as e:
        flash(f"Error deleting: {e}", "error")
        
    return redirect(url_for('admin.dashboard'))
