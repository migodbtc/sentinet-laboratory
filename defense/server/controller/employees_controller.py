from ._base_controller import BaseController
from resource.employees_resource import EmployeesResource

class EmployeesController(BaseController):
    def __init__(self, db_conn):
        resource = EmployeesResource(db_conn)
        super().__init__(resource)
