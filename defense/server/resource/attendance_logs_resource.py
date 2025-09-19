from ._base_resource import BaseResource

class AttendanceLogsResource(BaseResource):
    """Resource for attendance_logs table."""
    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.table = 'attendance_logs'
        self.fields = [
            'log_id', 'employee_id', 'shift_id', 'log_date',
            'time_in', 'time_out', 'hours_worked'
        ]
