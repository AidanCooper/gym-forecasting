class GymLoginException(Exception):
    """Raised if TheGym login process fails"""

    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"'www.thegymgroup.com/login/' login process failed"


class ColumnNotFoundException(Exception):
    """Raised if a specified column is not found in the dataframe"""

    def __init__(self, *args):
        super().__init__()
        self.column = args[0]

    def __str__(self):
        return f"Column name '{self.column}' not found in the dataframe."


class ColumnNotDatetimeException(Exception):
    """Raised if a specified column is not dtype Datetime"""

    def __init__(self, *args):
        super().__init__()
        self.column = args[0]

    def __str__(self):
        return f"Column name '{self.column}' is not a datetime."
