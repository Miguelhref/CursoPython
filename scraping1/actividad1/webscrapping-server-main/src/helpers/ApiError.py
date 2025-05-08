class ApiError(Exception):
    def __init__(self, **kwargs):
        self.message = kwargs.get('message', '')
        self.reason = kwargs.get('reason', '')
        self.status = kwargs.get('status', 400)
