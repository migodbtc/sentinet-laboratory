


import time
import mysql.connector
from mysql.connector import Error
import os
from flask import Flask, jsonify
from dotenv import load_dotenv

from controller.attendance_logs_controller import AttendanceLogsController
from controller.employees_controller import EmployeesController
from controller.payroll_controller import PayrollController
from controller.shifts_controller import ShiftsController

load_dotenv()

# Very, very slow interval database connection calling
# Because sometimes Docker takes a while to set up/boot up
# Edit as you wish though
def attempt_db_call():
    max_attempts = 10
    interval_seconds = 10
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
            time.sleep(interval_seconds)
            attempt += 1
    raise Exception("Could not connect to the database after several attempts.")

app = Flask(__name__)

# Create DB connection
db_conn = attempt_db_call()

# Instantiate controllers (pass db_conn directly)
attendance_logs_controller = AttendanceLogsController(db_conn)
employees_controller = EmployeesController(db_conn)
payroll_controller = PayrollController(db_conn)
shifts_controller = ShiftsController(db_conn)

# Register blueprints
app.register_blueprint(attendance_logs_controller.blueprint, url_prefix='/attendance_logs')
app.register_blueprint(employees_controller.blueprint, url_prefix='/employees')
app.register_blueprint(payroll_controller.blueprint, url_prefix='/payroll')
app.register_blueprint(shifts_controller.blueprint, url_prefix='/shifts')

@app.route("/")
def home():
    message = {"message": "Welcome to the Sentinet Laboratory API!"}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
