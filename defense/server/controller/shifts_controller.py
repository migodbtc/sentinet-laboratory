from ._base_controller import BaseController
from ..resource.shifts_resource import ShiftsResource

class ShiftsController(BaseController):
    def __init__(self, db_conn):
        resource = ShiftsResource(db_conn)
        super().__init__(resource)
