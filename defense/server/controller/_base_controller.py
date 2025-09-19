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
        return jsonify(self.resource.all())

    def show(self, id):
        return jsonify(self.resource.find(id))

    def store(self):
        data = request.get_json()
        return jsonify(self.resource.create(data)), 201

    def update(self, id):
        data = request.get_json()
        return jsonify(self.resource.update(id, data))

    def destroy(self, id):
        self.resource.delete(id)
        return '', 204
