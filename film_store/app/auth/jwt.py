from rest_framework.request import Request
from app.models import GeneralUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from app.api.api_request import APIRequest
from rest_framework_simplejwt.tokens import RefreshToken
import base64
import json
import hashlib
import hmac
from app.auth.token import Token
from datetime import datetime
import secrets
import uuid
from datetime import timedelta, datetime, timezone
from uuid import UUID
import os
from calendar import timegm
import jwt

class JWT(Token):
    def datetime_to_epoch(dt: datetime) -> int: return timegm(dt.utctimetuple())
    
    def verify_signature(self, input_header: str, input_payload: str, input_signature: str) -> bool:
        signature = hmac.new(
            self.secret_key.encode('utf-8'), 
            (input_header + '.' + input_payload).encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()

        return signature == input_signature
        

    def decode(self, token: str) -> GeneralUser:
        split_token = token.split('.')
        if len(split_token) != 3: raise Exception("Invalid token")
        header = split_token[0]
        payload = split_token[1]
        signature = split_token[2]

        if not self.verify_signature(header, payload, signature): return None

        payload_b = base64.b64decode(payload + '==') # add padding
        payload_str = payload_b.decode('utf-8')
        payload = json.loads(payload_str)
        
        try: 
            user = GeneralUser.objects.get(id=payload['user_id'])
            return user
        except GeneralUser.DoesNotExist: return None
        except Exception as e: return None


    
    def generate_jti(self):
        return UUID(bytes=os.urandom(16), version=4).hex
    
    def generate_exp(self):
        from_time: datetime = self.current_time
        lifetime: timedelta = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

        return JWT.datetime_to_epoch(from_time + lifetime)
    
    def generate_iat(self):
        return self.current_time.timestamp()
    
    def dict_to_base64_str(dict: dict) -> str:
        dict_str = json.dumps(dict, separators=(',', ':')) # remove whitespaces after :
        dict_b = dict_str.encode('utf-8')
        dict_b64 = base64.b64encode(dict_b)
        dict_b64_str = dict_b64.decode('utf-8')
        return dict_b64_str
    
    def encode(self, user: GeneralUser) -> str:
        header = {
            "alg":"HS256",
            "typ":"JWT"
        }
        payload = {
            "token_type":"access",
            "exp": self.generate_exp(),
            "iat": self.generate_iat(),
            "jti": self.generate_jti(),
            "user_id":user.id
        }

        header_b64_str: str = JWT.dict_to_base64_str(header)
        payload_b64_str: str = JWT.dict_to_base64_str(payload).rstrip('=') # just to make it pretty a bit

        signature = hmac.new(
            self.secret_key.encode('utf-8'), 
            (header_b64_str + '.' + payload_b64_str).encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()

        return header_b64_str + '.' + payload_b64_str + '.' + signature
        # return RefreshToken.for_user(user).access_token


    def authenticate(self, request: APIRequest) -> GeneralUser:
        auth = request.META['HTTP_AUTHORIZATION']
        split_auth = auth.split(' ')
        if len(split_auth) != 2: return None
        if split_auth[0] != 'Bearer': return None
        token = split_auth[1]
        return self.decode(token)
        # return JWTAuthentication().authenticate(request)[0]
        

    def __init__(self):
        self.secret_key: str = settings.SECRET_KEY
        if not self.secret_key: raise Exception("No secret key found")
        self.current_time = datetime.now(tz=timezone.utc)