from services.db import get_db_connection

def get_user_preference_context(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT personalization_enabled
        FROM users
        WHERE id = %s
        """,
        (user_id,)
    )
    user = cursor.fetchone()

    if not user or not user["personalization_enabled"]:
        cursor.close()
        conn.close()
        return None

    cursor.execute(
        """
        SELECT tag_name
        FROM preference_tags
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,)
    )
    tags = cursor.fetchall()

    cursor.close()
    conn.close()

    if not tags:
        return None

    return [tag["tag_name"] for tag in tags]