from rest_framework.response import Response
from typing import Dict
from enum import Enum
from http import HTTPStatus
from rest_framework import status
import datetime

class APIResponse(Response):
    
    def __init__(self, data: Dict = None, *args, **kwargs):
        super().__init__({
            "status": "success",
            "message": "",
            "data": data,
        }, *args, **kwargs)
    
    def error(self, message: str):
        self.data["status"] = "error"
        self.data["message"] = message
        self.data["data"] = None
        return self
    
    def set_status(self, status_code: status = status.HTTP_400_BAD_REQUEST):
        self.status_code = status_code
        return self
    
    def set_cookie(self, key: str, value: str = "", max_age: int | None = None, expires: str | datetime.datetime | None = None, path: str = "/", domain: str | None = None, secure: bool = False, httponly: bool = False, samesite: str = None):
        super().set_cookie(key, value, max_age, expires, path, domain, secure, httponly, samesite)
        return self
    
    def delete_cookie(self, key: str, path: str = "", domain: str | None = None):
        super().delete_cookie(key, path, domain)
        return self

    def is_success(self):
        return self.data["status"] == "success"

class APIResponseMissingIDError(APIResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error("id is required").set_status(status.HTTP_400_BAD_REQUEST)