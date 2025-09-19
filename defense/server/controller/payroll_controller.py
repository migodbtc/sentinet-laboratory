from ._base_controller import BaseController
from resource.payroll_resource import PayrollResource

class PayrollController(BaseController):
    def __init__(self, db_conn):
        resource = PayrollResource(db_conn)
        super().__init__(resource)
