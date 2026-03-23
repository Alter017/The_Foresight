from flask import Blueprint, request, jsonify
import bcrypt
from services.db import get_db_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST", "OPTIONS"])
def signup():
    if request.method == "OPTIONS":
        return '', 200

    try:
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirmPassword")

        if not username or not email or not password or not confirm_password:
            return jsonify({"error": "Username, email, password, and confirm password are required"}), 400

        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400

        conn = get_db_connection() #conn is the connection to db -> connect me to db
        cursor = conn.cursor(dictionary=True) #cursor is the tool tht lets u run queries thru tht connection -> give me sth tht can execute sql statemnts
        #dictionary = true makes results come back as dictionary
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))  #Meaning 'run this sql query'
        if cursor.fetchone(): #give one result row
            cursor.close()
            conn.close()
            return jsonify({"error": "Email already exists"}), 409

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Username already exists"}), 409

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        cursor.execute(
            """
            INSERT INTO users (email, username, password_hash)
            VALUES (%s, %s, %s)
            """,
            (email, username, password_hash)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Account created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@auth_bp.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return '', 200
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and Password are required"}), 400

        conn = get_db_connection() #conn is the connection to db -> connect me to db
        cursor = conn.cursor(dictionary=True) #cursor is the tool tht lets u run queries thru tht connection -> give me sth tht can execute sql statemnts
        #dictionary = true makes results come back as dictionary

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))  #Meaning 'run this sql query'
        user = cursor.fetchone() #this is checked later if it even exists 
            
        cursor.close()
        conn.close()

        if not user:
            return jsonify({"error": "Invalid email or password"}), 401
        
        if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
            return jsonify({"error": "Invalid email or password"}), 401
        
        #bcrypt.checkpw takes 2 inputs first = teh pass the user typed. the 2nd = hashed stored pass in db; it returns true if they match and false otherwise 
        #password.encode("utf-8") = takes passwords and encodes it 

        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"]
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logout successful"}), 200

@auth_bp.route("/account/username", methods=["PUT"])
def update_username():

    try:
        data = request.get_json()
        user_id = data.get("userId")
        new_username = data.get("username")

        if not new_username:
            return jsonify({"error": "username is required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if username is already taken by someone else
        cursor.execute(
            "SELECT id FROM users WHERE username = %s AND id != %s",
            (new_username, user_id)
        )

        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Username already exists"}), 409

        cursor.execute(
            "UPDATE users SET username = %s WHERE id = %s",
            (new_username, user_id)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Username updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@auth_bp.route("/account/password", methods=["PUT"])
def update_password():

    try:
        data = request.get_json()
        user_id = data.get("userId")
        current_password = data.get("currentPassword")
        new_password = data.get("newPassword")
        confirm_new_password = data.get("confirmNewPassword")

        if not current_password or not new_password or not confirm_new_password:
            return jsonify({
                "error": "currentPassword, newPassword, and confirmNewPassword are required"
            }), 400

        if new_password != confirm_new_password:
            return jsonify({"error": "New passwords do not match"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT password_hash FROM users WHERE id = %s",
            (user_id,)
        )
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return jsonify({"error": "User not found"}), 404

        password_matches = bcrypt.checkpw(
            current_password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        )

        if not password_matches:
            cursor.close()
            conn.close()
            return jsonify({"error": "Current password is incorrect"}), 401

        new_password_hash = bcrypt.hashpw(
            new_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute(
            """
            UPDATE users
            SET password_hash = %s
            WHERE id = %s
            """,
            (new_password_hash, user_id)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Password updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
