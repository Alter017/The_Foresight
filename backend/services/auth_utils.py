#This is a helper method; to help verify tht user is logged in for protected routes 
from flask import session, jsonify

def require_login():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    return None