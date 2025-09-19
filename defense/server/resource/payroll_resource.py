from ._base_resource import BaseResource

class PayrollResource(BaseResource):
    """Resource for payroll table."""
    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.table = 'payroll'
        self.fields = [
            'payroll_id', 'employee_id', 'period_start', 'period_end',
            'total_hours', 'gross_pay', 'deductions', 'net_pay', 'generated_at'
        ]
