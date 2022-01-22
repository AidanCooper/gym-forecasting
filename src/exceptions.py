class GymLoginException(Exception):
    """Raised if TheGym login process fails"""

    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"'www.thegymgroup.com/login/' login process failed"
