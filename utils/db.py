import mysql.connector
from flask import current_app

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
