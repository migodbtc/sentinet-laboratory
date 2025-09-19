import time 
import mysql.connector
from mysql.connector import Error
import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()  

def get_db_connection():
    max_attempts = 10
    attempt = 0
    while attempt < max_attempts:
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=os.getenv("DB_NAME"),
            )
            if conn.is_connected():
                print("Connected to MySQL database")
                return conn
        except Error as e:
            print(f"Attempt {attempt+1}: DB connection failed: {e}")
            time.sleep(3)
            attempt += 1
    raise Exception("Could not connect to the database after several attempts.")


app = Flask(__name__)

@app.route("/")
def home():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            result = cursor.fetchall()
            
            return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
