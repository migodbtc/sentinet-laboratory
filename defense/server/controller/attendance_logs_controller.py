from ._base_controller import BaseController
from ..resource.attendance_logs_resource import AttendanceLogsResource

class AttendanceLogsController(BaseController):
    def __init__(self, db_conn):
        resource = AttendanceLogsResource(db_conn)
        super().__init__(resource)
