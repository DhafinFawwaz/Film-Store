
from drf_yasg import openapi
from app.api.swagger.api_response_schema import APIResponseSchema

LoginFormBody = openapi.Schema(
    title='Login Form Parameters',
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description="The username of the user"),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description="The password of the user"),
    }
)

RegisterFormBody = openapi.Schema(
    title='Register Form Parameters',
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description="The username of the user"),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description="The email of the user"),
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="The first name of the user"),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="The last name of the user"),
        'password1': openapi.Schema(type=openapi.TYPE_STRING, description="The password of the user"),
        'password2': openapi.Schema(type=openapi.TYPE_STRING, description="Confirm the password for the user"),
    }
)


# Login Response
LoginResponseSchema = APIResponseSchema.copy()
LoginResponseSchema['data'] = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'username': openapi.Schema(type=openapi.TYPE_STRING, description="The title of the film"),
    'token': openapi.Schema(type=openapi.TYPE_STRING, description="The director of the film"),
})
LoginResponse = openapi.Schema(
    title='Login Response',
    type=openapi.TYPE_OBJECT,
    properties=LoginResponseSchema
)

# Register Response
RegisterResponseSchema = APIResponseSchema.copy()
RegisterResponseSchema['data'] = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'username': openapi.Schema(type=openapi.TYPE_STRING, description="The username of the user"),
    'email': openapi.Schema(type=openapi.TYPE_STRING, description="The email of the user"),
    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="The first name of the user"),
    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="The last name of the user"),
})
RegisterResponse = openapi.Schema(
    title='Register Response',
    type=openapi.TYPE_OBJECT,
    properties=RegisterResponseSchema
)

# Self Response
SelfResponseSchema = APIResponseSchema.copy()
SelfResponseSchema['data'] = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'username': openapi.Schema(type=openapi.TYPE_STRING, description="The username of the user"),
    'token': openapi.Schema(type=openapi.TYPE_STRING, description="The token of the user"),
})
SelfResponse = openapi.Schema(
    title='Self Response',
    type=openapi.TYPE_OBJECT,
    properties=SelfResponseSchema
)

# Users Response
UsersResponseSchema = APIResponseSchema.copy()
UsersResponseSchema['data'] = openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'id': openapi.Schema(type=openapi.TYPE_STRING, description="The id of the user"),
    'username': openapi.Schema(type=openapi.TYPE_STRING, description="The username of the user"),
    'email': openapi.Schema(type=openapi.TYPE_STRING, description="The email of the user"),
    'balance': openapi.Schema(type=openapi.TYPE_INTEGER, description="The balance of the user"),
    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="The first name of the user"),
    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="The last name of the user"),
}))
UsersResponse = openapi.Schema(
    title='Users Response',
    type=openapi.TYPE_OBJECT,
    properties=UsersResponseSchema
)

# UserDetail Response
UserDetailResponseSchema = APIResponseSchema.copy()
UserDetailResponseSchema['data'] = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'id': openapi.Schema(type=openapi.TYPE_STRING, description="The id of the user"),
    'username': openapi.Schema(type=openapi.TYPE_STRING, description="The username of the user"),
    'email': openapi.Schema(type=openapi.TYPE_STRING, description="The email of the user"),
    'balance': openapi.Schema(type=openapi.TYPE_INTEGER, description="The balance of the user"),
    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="The first name of the user"),
    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="The last name of the user"),
})
UserDetailResponse = openapi.Schema(
    title='User Detail Response',
    type=openapi.TYPE_OBJECT,
    properties=UserDetailResponseSchema
)


# UserBalance Response
# Same as UserDetailResponseSchema
UserBalanceResponse = UserDetailResponse

# UserDelete Response
# Same as UserDetailResponseSchema
UserDeleteResponse = UserDetailResponse

# Logout Response
LogoutResponseSchema = UserDetailResponse