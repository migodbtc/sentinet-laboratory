from flask import Blueprint, request, jsonify

class BaseController:
    """Base Controller class for HTTP logic."""
    def __init__(self, resource):
        self.resource = resource
        self.blueprint = Blueprint(self.__class__.__name__, __name__)
        self.register_routes()

    def register_routes(self):
        bp = self.blueprint
        bp.add_url_rule('/', 'index', self.index, methods=['GET'])
        bp.add_url_rule('/<int:id>', 'show', self.show, methods=['GET'])
        bp.add_url_rule('/', 'store', self.store, methods=['POST'])
        bp.add_url_rule('/<int:id>', 'update', self.update, methods=['PUT', 'PATCH'])
        bp.add_url_rule('/<int:id>', 'destroy', self.destroy, methods=['DELETE'])

    def index(self):
        """
        Returns all records from the resource table.
        Parameters:
            None

        Example:
            GET /employees
        """
        return jsonify(self.resource.all())

    def show(self, id):
        """
        Finds a record by primary key.
        Parameters:
            id (int): The primary key value to search for.

        Example:
            GET /employees/1
        """
        return jsonify(self.resource.find(id))

    def store(self):
        """
        Creates a new record in the resource table.
        Parameters:
            data (dict, JSON body): Dictionary of column-value pairs to insert.

        Example:
            POST /employees
            Body: {
                "first_name": "Eve",
                "last_name": "Garcia",
                "position": "DevOps Engineer",
                "base_salary": 60000.00,
                "hire_date": "2025-09-19"
            }
        """
        data = request.get_json()
        return jsonify(self.resource.create(data)), 201

    def update(self, id):
        """
        Updates a record by primary key.
        Parameters:
            id (int): The primary key value to update.
            data (dict, JSON body): Dictionary of column-value pairs to update.

        Example:
            PUT /employees/2
            Body: {
                "base_salary": 42000.00,
                "position": "HR Lead"
            }
        """
        data = request.get_json()
        return jsonify(self.resource.update(id, data))

    def destroy(self, id):
        """
        Deletes a record by primary key.
        Parameters:
            id (int): The primary key value to delete.

        Example:
            DELETE /employees/4
        """
        self.resource.delete(id)
        return '', 204
