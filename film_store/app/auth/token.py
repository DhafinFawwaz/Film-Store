from app.models import GeneralUser
from app.api.api_request import APIRequest
from abc import ABC

class Token(ABC):
    def encode(user: GeneralUser) -> str: pass
    def decode(token: str) -> GeneralUser: pass
    def authenticate(request: APIRequest) -> GeneralUser: pass
        