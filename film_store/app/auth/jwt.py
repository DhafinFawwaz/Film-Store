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

class JWT():

    def decode_payload(payload: str) -> dict:
        payload = base64.b64decode(payload + '==')
        payload = payload.decode('utf-8')
        payload = json.loads(payload)
        return payload
    
    def verify_signature(input_header: str, input_payload: str, input_signature: str) -> bool:
        return True

    def decode(token: str) -> GeneralUser:
        split_token = token.split('.')
        if len(split_token) != 3: raise Exception("Invalid token")
        header = split_token[0]
        payload = split_token[1]
        signature = split_token[2]

        if not JWT.verify_signature(header, payload, signature): return None

        payload = JWT.decode_payload(payload)
        try:
            user = GeneralUser.objects.get(id=payload['user_id'])
            return user
        except GeneralUser.DoesNotExist:
            return None
        except Exception as e:
            return None
    
    def encode(user: GeneralUser) -> str:
        # secret_key = settings.SECRET_KEY
        # if not secret_key: raise Exception("No secret key found")

        # header = {
        #     "alg": "HS256",
        #     "typ": "JWT"
        # }

        # payload = {
        #     "user_id": user.id,
        # }
        
        # return header + '.' + payload + '.' + signature
        return RefreshToken.for_user(user).access_token
    
    def authenticate(request: APIRequest) -> GeneralUser:
        auth = request.META['HTTP_AUTHORIZATION']
        split_auth = auth.split(' ')
        if len(split_auth) != 2: return None
        if split_auth[0] != 'Bearer': return None
        token = split_auth[1]
        # return JWT.decode(token)
        return JWTAuthentication().authenticate(request)[0]
        