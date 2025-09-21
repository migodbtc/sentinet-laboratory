


import time
import mysql.connector
from mysql.connector import Error
import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask import request, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

from controller.attendance_logs_controller import AttendanceLogsController
from controller.employees_controller import EmployeesController
from controller.payroll_controller import PayrollController
from controller.shifts_controller import ShiftsController
from controller.users_controller import UsersController

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
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Create DB connection
db_conn = attempt_db_call()

# Instantiate controllers (pass db_conn directly)
attendance_logs_controller = AttendanceLogsController(db_conn)
employees_controller = EmployeesController(db_conn)
payroll_controller = PayrollController(db_conn)
shifts_controller = ShiftsController(db_conn)
users_controller = UsersController(db_conn)

# Register blueprints
app.register_blueprint(attendance_logs_controller.blueprint, url_prefix='/attendance_logs')
app.register_blueprint(employees_controller.blueprint, url_prefix='/employees')
app.register_blueprint(payroll_controller.blueprint, url_prefix='/payroll')
app.register_blueprint(shifts_controller.blueprint, url_prefix='/shifts')
app.register_blueprint(users_controller.blueprint, url_prefix='/users')

@app.route("/")
def home():
    message = {"message": "Welcome to the Sentinet Laboratory API!"}
    return jsonify(message)

@app.route("/login", methods=["POST"])
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    with db_conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

    if user and check_password_hash(user["password_hash"], password):
        access_token = create_access_token(identity=user["user_id"])
        refresh_token = create_refresh_token(identity=user["user_id"])

        with db_conn.cursor() as cursor:
            cursor.execute("UPDATE users SET refresh_token = %s WHERE user_id = %s", (refresh_token, user["user_id"]))
            db_conn.commit()

        return jsonify(access_token=access_token, refresh_token=refresh_token), 200

    return jsonify({"message": "Invalid credentials"}), 401
    
@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    print(f"Logging out user_id: {user_id}")  # Debugging log

    # Clear refresh token in the database
    with db_conn.cursor() as cursor:
        cursor.execute("UPDATE `users` SET `refresh_token` = NULL WHERE `user_id` = %s", (user_id,))
        db_conn.commit()

    return jsonify({"message": "Logged out successfully"}), 200

@app.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return make_response(jsonify({"message": "Refresh token is required"}), 400)

    # Verify the refresh token against the database
    with db_conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM users WHERE refresh_token = %s", (refresh_token,))
        user = cursor.fetchone()

    # If user found with the provided refresh token, issue a new access token
    if user:
        new_access_token = create_access_token(identity=user["user_id"])
        return jsonify(access_token=new_access_token), 200

    return make_response(jsonify({"error": "Invalid refresh token"}), 401)

@app.route("/register", methods=["POST"])
def register():
    """
    Handles user registration.
    Delegates the logic to the UsersController.
    """
    return users_controller.store()
		

if __name__ == "__main__":
    app.run(debug=True)
