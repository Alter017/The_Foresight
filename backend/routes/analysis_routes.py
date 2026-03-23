#Blueprint: template of operations that can be registered with main flask app
from flask import Blueprint, request, jsonify 
from services.llm_service import generate_pros_cons
from services.db import get_db_connection

analysis_bp = Blueprint("analysis", __name__) #create bp object named analysis

@analysis_bp.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == "OPTIONS":
        return '', 200
    try:
        data = request.get_json()

        title = data.get("title")
        description = data.get("description")
        options = data.get("options")
        user_id = data.get("user_id")

        if not title or not description:
            return jsonify({"error": "Title and description required"}), 400

        if not options or not isinstance(options, list):
            return jsonify({"error": "Options must be a list"}), 400

        reflection_context = ""

        if user_id:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT reflection_note 
                FROM scenarios 
                WHERE user_id = %s AND reflection_note IS NOT NULL
                ORDER BY created_at DESC
                LIMIT 5
            """, (user_id,))

            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            if rows:
                reflection_context = """
User behavior patterns (from past reflections):
- Learn from these patterns
- Avoid repeating past regrets
- Reinforce positive decisions

"""
                for r in rows:
                    reflection_context += f"- {r['reflection_note']}\n"

            scenario = f"""
You are an intelligent decision-making assistant.

If user reflections are provided:
- Use them to personalize advice
- Refer to them explicitly when relevant
- Highlight patterns (e.g. regrets, preferences)
- Warn if a choice contradicts past reflections
- Reinforce good past decisions

{reflection_context}

Current scenario:
{title}: {description}
"""

        all_results = []

        for opt in options:
            result = generate_pros_cons(scenario, [opt])
            print("LLM result:", result)
            if isinstance(result, list):
                all_results.extend(result)
            else:
                all_results.append(result)

        return jsonify(all_results)
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
