from ._base_resource import BaseResource

class ShiftsResource(BaseResource):
    """Resource for shifts table."""
    def __init__(self):
        super().__init__()
        self.table = 'shifts'
        self.fields = [
            'shift_id', 'shift_name', 'start_time', 'end_time'
        ]
