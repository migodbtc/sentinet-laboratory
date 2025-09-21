from ._base_controller import BaseController
from resource.users_resource import UsersResource
from flask import request, jsonify

class UsersController(BaseController):
    """Controller for users resource."""
    def __init__(self, db_connection):
        resource = UsersResource(db_connection)
        super().__init__(resource)

    def store(self):
        data = request.get_json()

        if not data.get('username') or not data.get('password'):
            return jsonify({"message": "Username and password are required"}), 400

        existing_user = self.resource.find_by_field('username', data['username'])
        if existing_user:
            return jsonify({"message": "Username already exists"}), 409

        self.resource.create(data)
        return jsonify({"message": "User registered successfully"}), 201