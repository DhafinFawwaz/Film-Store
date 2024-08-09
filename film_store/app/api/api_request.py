from rest_framework.request import Request

class APIRequest(Request):
    def __init__(self, request: Request):
        self.token: str = None
        self.COOKIES: dict = {}
        self.headers: dict = {}
        self.META: dict = {}