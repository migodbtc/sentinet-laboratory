import mysql.connector
import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()  

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()
cursor.execute("SELECT NOW()")
print("DB Time:", cursor.fetchone())


app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask is running in .venv!"

if __name__ == "__main__":
    app.run(debug=True)
