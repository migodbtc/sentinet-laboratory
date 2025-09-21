from ._base_resource import BaseResource

class UsersResource(BaseResource):
    """Resource for users table."""
    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.table = 'users'
        self.fields = [
            'user_id', 'username', 'password_hash', 'role', 'created_at', 'refresh_token'
        ]