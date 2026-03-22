from flask import Blueprint, request, jsonify, session
from services.db import get_db_connection
from services.auth_utils import require_login

preference_bp = Blueprint("preferences", __name__)

@preference_bp.route("/settings", methods=["PUT"])
def update_personalization_setting():
    auth_error = require_login()
    if auth_error:
        return auth_error

    try:
        data = request.get_json()
        personalization_enabled = data.get("personalization_enabled")

        if personalization_enabled is None:
            return jsonify({"error": "personalization_enabled is required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE users
            SET personalization_enabled = %s
            WHERE id = %s
            """,
            (personalization_enabled, session["user_id"])
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Personalization setting updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@preference_bp.route("/tags", methods=["GET"])
def get_preference_tags():
    auth_error = require_login()
    if auth_error:
        return auth_error

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, tag_name, created_at
            FROM preference_tags
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (session["user_id"],)
        )

        tags = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({"tags": tags}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@preference_bp.route("/tags", methods=["POST"])
def add_preference_tag():
    auth_error = require_login()
    if auth_error:
        return auth_error

    try:
        data = request.get_json()
        tag_name = data.get("tag_name")

        if not tag_name:
            return jsonify({"error": "tag_name is required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO preference_tags (user_id, tag_name)
            VALUES (%s, %s)
            """,
            (session["user_id"], tag_name)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Preference tag added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@preference_bp.route("/tags/<int:tag_id>", methods=["PUT"])
def update_preference_tag(tag_id):
    auth_error = require_login()
    if auth_error:
        return auth_error

    try:
        data = request.get_json()
        tag_name = data.get("tag_name")

        if not tag_name:
            return jsonify({"error": "tag_name is required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE preference_tags
            SET tag_name = %s
            WHERE id = %s AND user_id = %s
            """,
            (tag_name, tag_id, session["user_id"])
        )

        conn.commit()

        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Tag not found"}), 404

        cursor.close()
        conn.close()

        return jsonify({"message": "Preference tag updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@preference_bp.route("/tags/<int:tag_id>", methods=["DELETE"])
def delete_preference_tag(tag_id):
    auth_error = require_login()
    if auth_error:
        return auth_error

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM preference_tags
            WHERE id = %s AND user_id = %s
            """,
            (tag_id, session["user_id"])
        )

        conn.commit()

        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Tag not found"}), 404

        cursor.close()
        conn.close()

        return jsonify({"message": "Preference tag deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500