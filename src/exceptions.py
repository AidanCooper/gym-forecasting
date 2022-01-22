class GymLoginException(Exception):
    """Raised if TheGym login process fails"""

    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"'www.thegymgroup.com/login/' login process failed."


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


class LimitException(Exception):
    """Raised if specified plotting limit is invalid"""

    def __init__(self, *args):
        super().__init__()
        self.limit = args[0]

    def __str__(self):
        return f"Plotting limit '{self.limit}' must be between 0.0-100.0 inclusive."


class ConfidenceIntervalException(Exception):
    """Raised if specified confidence interval is invalid"""

    def __init__(self, *args):
        super().__init__()
        self.ci = args[0]

    def __str__(self):
        return f"Confidence interval '{self.ci}' must be between 0.0-1.0 exclusive."
