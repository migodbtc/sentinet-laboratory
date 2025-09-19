from ._base_resource import BaseResource

class EmployeesResource(BaseResource):
    """Resource for employees table."""
    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.table = 'employees'
        self.fields = [
            'employee_id', 'first_name', 'last_name', 'position',
            'base_salary', 'hire_date'
        ]
