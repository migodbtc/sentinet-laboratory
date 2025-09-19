from ._base_resource import BaseResource

class AttendanceLogsResource(BaseResource):
    """Resource for attendance_logs table."""
    def __init__(self):
        super().__init__()
        self.table = 'attendance_logs'
        self.fields = [
            'log_id', 'employee_id', 'shift_id', 'log_date',
            'time_in', 'time_out', 'hours_worked'
        ]
