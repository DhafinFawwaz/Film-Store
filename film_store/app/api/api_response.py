from rest_framework.response import Response
from typing import Dict
from enum import Enum
from http import HTTPStatus
from rest_framework import status

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
        return self
    
    def set_status(self, status_code: status = status.HTTP_400_BAD_REQUEST):
        self.status_code = status_code
        return self

class APIResponseMissingIDError(APIResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error("id is required").set_status(status.HTTP_400_BAD_REQUEST)