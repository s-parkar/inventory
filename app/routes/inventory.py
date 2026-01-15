from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import supabase
import os

inventory_bp = Blueprint('inventory', __name__)

def get_user():
    token = session.get('access_token')
    if not token or not supabase:
        return None
    try:
        user = supabase.auth.get_user(token)
        return user
    except Exception as e:
        return None

@inventory_bp.route('/')
def home():
    if get_user():
        return redirect(url_for('inventory.dashboard'))
    return redirect(url_for('auth.login'))

@inventory_bp.route('/dashboard')
def dashboard():
    user = get_user()
    if not user:
        return redirect(url_for('auth.login'))
        
    app_version = os.getenv("APP_VERSION", "1.0.0")

    # Fetch Products
    try:
        products_res = supabase.table('products').select("*").order('created_at', desc=True).execute()
        products = products_res.data
    except Exception as e:
        flash(f"Error fetching products: {e}", "error")
        products = []

    # Fetch Logs
    try:
        logs_res = supabase.table('logs').select("*").order('timestamp', desc=True).limit(20).execute()
        logs = logs_res.data
    except Exception as e:
        flash(f"Error fetching logs: {e}", "error")
        logs = []

    return render_template('dashboard.html', products=products, logs=logs, user=user, version=app_version)

@inventory_bp.route('/add_product', methods=['POST'])
def add_product():
    if not get_user(): return redirect(url_for('auth.login'))
    
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')
    
    try:
        data = {"name": name, "quantity": int(quantity), "price": float(price)}
        supabase.table('products').insert(data).execute()
        
        # Log action
        log_data = {"action": f"Added product: {name} (Qty: {quantity})"}
        supabase.table('logs').insert(log_data).execute()
        
        flash("Product added successfully!", "success")
    except Exception as e:
        flash(f"Error adding product: {e}", "error")
        
    return redirect(url_for('inventory.dashboard'))

@inventory_bp.route('/buy_product/<product_id>', methods=['POST'])
def buy_product(product_id):
    if not get_user(): return redirect(url_for('auth.login'))
    
    try:
        # Check current Qty
        prod = supabase.table('products').select("name, quantity").eq("id", product_id).single().execute()
        current_qty = prod.data.get('quantity', 0)
        name = prod.data.get('name')
        
        if current_qty > 0:
            supabase.table('products').update({"quantity": current_qty - 1}).eq("id", product_id).execute()
            
            # Log action
            log_data = {"action": f"Bought product: {name}"}
            supabase.table('logs').insert(log_data).execute()
            
            flash(f"Bought {name}!", "success")
        else:
            flash(f"Out of stock: {name}", "error")
            
    except Exception as e:
        flash(f"Error buying product: {e}", "error")
        
    return redirect(url_for('inventory.dashboard'))
