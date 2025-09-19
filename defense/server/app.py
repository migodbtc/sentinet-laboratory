


import time
import mysql.connector
from mysql.connector import Error
import os
from flask import Flask, jsonify
from dotenv import load_dotenv

# print location on startup
print(f"Current working directory: {os.getcwd()}")
# parent directories (1 layer up then 2 layer up)
print(f"Parent directory (1 layer up): {os.path.dirname(os.getcwd())}")
print(f"Parent directory (2 layers up): {os.path.dirname(os.path.dirname(os.getcwd()))}")

# Import resources and controllers (relative imports)
from .resource.attendance_logs_resource import AttendanceLogsResource
from .resource.employees_resource import EmployeesResource
from .resource.payroll_resource import PayrollResource
from .resource.shifts_resource import ShiftsResource

from .controller.attendance_logs_controller import AttendanceLogsController
from .controller.employees_controller import EmployeesController
from .controller.payroll_controller import PayrollController
from .controller.shifts_controller import ShiftsController

load_dotenv()

def attempt_db_call():
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

# Create DB connection
db_conn = attempt_db_call()

# Instantiate resources
attendance_logs_resource = AttendanceLogsResource(db_conn)
employees_resource = EmployeesResource(db_conn)
payroll_resource = PayrollResource(db_conn)
shifts_resource = ShiftsResource(db_conn)

# Instantiate controllers
attendance_logs_controller = AttendanceLogsController(attendance_logs_resource)
employees_controller = EmployeesController(employees_resource)
payroll_controller = PayrollController(payroll_resource)
shifts_controller = ShiftsController(shifts_resource)

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
