from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import supabase

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not supabase:
             flash("Supabase not configured.", "error")
             return render_template('login.html')

        try:
            # 1. Sign In
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            session['access_token'] = res.session.access_token
            user_id = res.user.id
            
            # 2. Get Role
            try:
                role_res = supabase.table('user_roles').select('role').eq('user_id', user_id).single().execute()
                role = role_res.data.get('role', 'user')
            except:
                role = 'user' # Default
            
            session['role'] = role
            flash(f"Welcome back, {role.capitalize()}!", "success")

            # 3. Redirect based on role
            if role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif role == 'supplier':
                return redirect(url_for('supplier.dashboard'))
            else:
                return redirect(url_for('inventory.dashboard'))

        except Exception as e:
            flash(f"Login failed: {str(e)}", "error")
            print(e)
            
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'user')

        try:
            # 1. Sign Up
            res = supabase.auth.sign_up({"email": email, "password": password})
            
            if res.user:
                # 2. Assign Role (Manual insert for demo)
                # In strict production, this should be a Trigger or Admin-only function
                user_id = res.user.id
                supabase.table('user_roles').insert({"user_id": user_id, "role": role}).execute()
                
                flash("Registration successful! Please Log In.", "success")
                return redirect(url_for('auth.login'))
            else:
                flash("Check your email for confirmation.", "info")
                return redirect(url_for('auth.login'))
                
        except Exception as e:
            flash(f"Registration failed: {str(e)}", "error")

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for('auth.login'))
