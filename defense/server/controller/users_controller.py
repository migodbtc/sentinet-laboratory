from ._base_controller import BaseController
from resource.users_resource import UsersResource

class UsersController(BaseController):
    """Controller for users resource."""
    def __init__(self, db_connection):
        resource = UsersResource(db_connection)
        super().__init__(resource)