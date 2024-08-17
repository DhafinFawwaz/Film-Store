from rest_framework.request import Request
from app.models import GeneralUser

class APIRequest(Request):
    def __init__(self):
        self.token: str = None
        self.COOKIES: dict = {}
        self.headers: dict = {}
        self.META: dict = {}
        self.user: GeneralUser = None