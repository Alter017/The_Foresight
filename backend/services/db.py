import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="foresight_user",
        password="foresight_pass",
        database="foresight"
    )
    return connection