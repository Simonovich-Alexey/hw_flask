class HttpError(Exception):
    def __init__(self, status_code: int, massage: str):
        self.status_code = status_code
        self.massage = massage
