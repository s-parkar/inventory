from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import supabase
import os

supplier_bp = Blueprint('supplier', __name__, url_prefix='/supplier')

def is_supplier():
    role = session.get('role')
    return role == 'supplier'

@supplier_bp.before_request
def check_supplier():
    if not session.get('access_token'):
        return redirect(url_for('auth.login'))
    if not is_supplier():
        flash("Access Denied: Suppliers only.", "error")
        # If admin tries to access, maybe allow? For now strict.
        if session.get('role') == 'admin': return None 
        return redirect(url_for('inventory.dashboard'))

@supplier_bp.route('/dashboard')
def dashboard():
    app_version = os.getenv("APP_VERSION", "1.0.0")
    user_id = supabase.auth.get_user(session.get('access_token')).user.id
    
    # Fetch My Products
    try:
        # Assuming RLS allows seeing own products or we filter by supplier_id if we added that column
        # For this demo, let's assume suppliers see ALL products but can only "Add" new ones.
        # Or better, filter if we added supplier_id to schema (we did in step 115).
        products_res = supabase.table('products').select("*").eq('supplier_id', user_id).order('created_at', desc=True).execute()
        products = products_res.data
    except Exception as e:
        products = []

    return render_template('supplier_dashboard.html', products=products, version=app_version)

@supplier_bp.route('/add_product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')
    user_id = supabase.auth.get_user(session.get('access_token')).user.id
    
    try:
        data = {
            "name": name, 
            "quantity": int(quantity), 
            "price": float(price),
            "supplier_id": user_id
        }
        supabase.table('products').insert(data).execute()
        
        # Log action
        log_data = {"action": f"Supplier added: {name} (Qty: {quantity})"}
        supabase.table('logs').insert(log_data).execute()
        
        flash("Product added successfully!", "success")
    except Exception as e:
        flash(f"Error adding product: {e}", "error")
        
    return redirect(url_for('supplier.dashboard'))
