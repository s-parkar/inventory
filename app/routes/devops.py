from flask import Blueprint, jsonify, session
from app import supabase
import os

devops_bp = Blueprint('devops', __name__)

@devops_bp.route('/health')
def health():
    return {'status': 'UP'}

@devops_bp.route('/metrics')
def metrics():
    return """
    app_requests_total 10
    app_errors_total 0
    """

@devops_bp.route('/simulate_error')
def simulate_error():
    raise Exception('Simulated failure')
