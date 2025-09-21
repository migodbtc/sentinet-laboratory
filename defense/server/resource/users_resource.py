from werkzeug.security import generate_password_hash
from ._base_resource import BaseResource

class UsersResource(BaseResource):
    """Resource for users table."""
    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.table = 'users'
        self.fields = [
            'user_id', 'username', 'password_hash', 'role', 'created_at', 'refresh_token'
        ]

    def create(self, data):
        """
        Creates a new user with a hashed password.
        Parameters:
            data (dict): Dictionary containing 'username', 'password', and optional 'role'.

        Example:
            users_resource.create({
                'username': 'new.user',
                'password': 'secure_password',
                'role': 'employee'
            })
        """
        if 'password' in data:
            data['password_hash'] = generate_password_hash(data.pop('password'))
        return super().create(data)