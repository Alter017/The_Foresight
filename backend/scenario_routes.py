from flask import Blueprint, jsonify, session, request
from services.auth_utils import require_login
from services.db import get_db_connection
import json 

scenario_bp = Blueprint("scenarios", __name__)

@scenario_bp.route("/save", methods=["POST"])
def save_scenario():
    auth_error = require_login()
    if auth_error:
        return auth_error

    try:
        data = request.get_json()

        title = data.get("title")
        scenario_text = data.get("scenario_text")
        options = data.get("options")
        pros_cons = data.get("pros_cons")

        if not title or not scenario_text or not options:
            return jsonify({"error": "Title, scenario_text, and options are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO scenarios (user_id, title, scenario_text, options_json, pros_cons_json)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                session["user_id"],
                title,
                scenario_text,
                json.dumps(options), #this is why we imported json
                json.dumps(pros_cons) if pros_cons else None
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Scenario saved successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@scenario_bp.route("/history", methods=["GET"])
def get_history():
    auth_error = require_login()
    if auth_error:
        return auth_error

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, title, scenario_text, final_decision_text, created_at
            FROM scenarios
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (session["user_id"],)
        )

        scenarios = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({"scenarios": scenarios}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@scenario_bp.route("/<int:scenario_id>", methods=["GET"])
def get_scenario_details(scenario_id):
    auth_error = require_login()
    if auth_error:
        return auth_error

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, user_id, title, scenario_text, options_json, pros_cons_json,
                   final_decision_text, reflection_note, created_at, updated_at
            FROM scenarios
            WHERE id = %s AND user_id = %s
            """,
            (scenario_id, session["user_id"])
        )

        scenario = cursor.fetchone()

        cursor.close()
        conn.close()

        if not scenario:
            return jsonify({"error": "Scenario not found"}), 404

        return jsonify({"scenario": scenario}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@scenario_bp.route("/<int:scenario_id>/final-decision", methods=["PUT"])
def update_final_decision(scenario_id):
    auth_error = require_login()
    if auth_error:
        return auth_error

    try:
        data = request.get_json()
        final_decision_text = data.get("final_decision_text")

        if not final_decision_text:
            return jsonify({"error": "final_decision_text is required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE scenarios
            SET final_decision_text = %s
            WHERE id = %s AND user_id = %s
            """,
            (final_decision_text, scenario_id, session["user_id"])
        )

        conn.commit()

        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Scenario not found"}), 404

        cursor.close()
        conn.close()

        return jsonify({"message": "Final decision updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@scenario_bp.route("/<int:scenario_id>/reflection-note", methods=["PUT"])
def update_reflection_note(scenario_id):
    auth_error = require_login()
    if auth_error:
        return auth_error

    try:
        data = request.get_json()
        reflection_note = data.get("reflection_note")

        if reflection_note is None:
            return jsonify({"error": "reflection_note is required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE scenarios
            SET reflection_note = %s
            WHERE id = %s AND user_id = %s
            """,
            (reflection_note, scenario_id, session["user_id"])
        )

        conn.commit()

        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Scenario not found"}), 404

        cursor.close()
        conn.close()

        return jsonify({"message": "Reflection note updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@scenario_bp.route("/<int:scenario_id>/reflection-note", methods=["DELETE"])
def delete_reflection_note(scenario_id):
    auth_error = require_login()
    if auth_error:
        return auth_error

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE scenarios
            SET reflection_note = NULL
            WHERE id = %s AND user_id = %s
            """,
            (scenario_id, session["user_id"])
        )

        conn.commit()

        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Scenario not found"}), 404

        cursor.close()
        conn.close()

        return jsonify({"message": "Reflection note deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500