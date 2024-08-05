from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view
from app.api.api_response import APIResponse
from app.models import GeneralUser
from app.serializers import GeneralUserSerializer
from app.api.protected import protected, admin_only

@api_view(['POST'])
@admin_only
def seed_db(request, *args, **kwargs):
    print("Seeding database..")
    
    