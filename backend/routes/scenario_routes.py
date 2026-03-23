from flask import Blueprint, jsonify, request
from services.auth_utils import require_login
from services.db import get_db_connection
import json 

scenario_bp = Blueprint("scenarios", __name__)

@scenario_bp.route("/save", methods=["POST"])
def save_scenario():
    try:
        data = request.get_json()

        user_id = data.get("user_id")
        title = data.get("title")
        scenario_text = data.get("scenario_text")
        options = data.get("options")
        pros_cons = data.get("pros_cons")

        if not user_id:
            return jsonify({"error": "user_id required"}), 401

        if not title or not scenario_text or not options:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO scenarios (user_id, title, scenario_text, options_json, pros_cons_json)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                user_id,
                title,
                scenario_text,
                json.dumps(options),
                json.dumps(pros_cons) if pros_cons else None
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        scenario_id = cursor.lastrowid

        return jsonify({
            "message": "Scenario saved successfully",
            "scenario_id": scenario_id
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@scenario_bp.route("/history", methods=["GET"])
def get_history():
    try:
        user_id = request.args.get("user_id")

        if not user_id:
            return jsonify({"error": "user_id required"}), 400

        user_id = int(user_id)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, title, scenario_text, options_json, pros_cons_json,
                final_decision_text, reflection_note, created_at
            FROM scenarios
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        scenarios = cursor.fetchall()

        for s in scenarios:
            s["options"] = json.loads(s["options_json"]) if s["options_json"] else []
            s["pros_cons"] = json.loads(s["pros_cons_json"]) if s["pros_cons_json"] else []

        cursor.close()
        conn.close()

        return jsonify({"scenarios": scenarios}), 200

    except Exception as e:
        print("HISTORY ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
    
# @scenario_bp.route("/<int:scenario_id>", methods=["GET"])
# def get_scenario_details(scenario_id):
#     auth_error = require_login()
#     if auth_error:
#         return auth_error

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)

#         cursor.execute(
#             """
#             SELECT id, user_id, title, scenario_text, options_json, pros_cons_json,
#                    final_decision_text, reflection_note, created_at, updated_at
#             FROM scenarios
#             WHERE id = %s AND user_id = %s
#             """,
#             (scenario_id, session["user_id"])
#         )

#         scenario = cursor.fetchone()

#         cursor.close()
#         conn.close()

#         if not scenario:
#             return jsonify({"error": "Scenario not found"}), 404

#         return jsonify({"scenario": scenario}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
@scenario_bp.route("/<int:scenario_id>/final-decision", methods=["PUT"])
def update_final_decision(scenario_id):
    try:
        data = request.get_json()

        user_id = data.get("user_id")
        final_decision_text = data.get("final_decision_text")

        if not user_id:
            return jsonify({"error": "user_id required"}), 401

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
            (final_decision_text, scenario_id, user_id)
        )

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Scenario not found"}), 404

        cursor.close()
        conn.close()

        return jsonify({"message": "Decision updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@scenario_bp.route("/<int:scenario_id>/reflection-note", methods=["PUT"])
def update_reflection_note(scenario_id):
    try:
        data = request.get_json()

        user_id = data.get("user_id")
        reflection_note = data.get("reflection_note")

        if not user_id:
            return jsonify({"error": "user_id required"}), 401

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
            (reflection_note, scenario_id, user_id)
        )

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Scenario not found"}), 404

        cursor.close()
        conn.close()

        return jsonify({"message": "Reflection updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @scenario_bp.route("/<int:scenario_id>/reflection-note", methods=["DELETE"])
# def delete_reflection_note(scenario_id):
#     auth_error = require_login()
#     if auth_error:
#         return auth_error

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         cursor.execute(
#             """
#             UPDATE scenarios
#             SET reflection_note = NULL
#             WHERE id = %s AND user_id = %s
#             """,
#             (scenario_id, session["user_id"])
#         )

#         conn.commit()

#         if cursor.rowcount == 0:
#             cursor.close()
#             conn.close()
#             return jsonify({"error": "Scenario not found"}), 404

#         cursor.close()
#         conn.close()

#         return jsonify({"message": "Reflection note deleted successfully"}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
