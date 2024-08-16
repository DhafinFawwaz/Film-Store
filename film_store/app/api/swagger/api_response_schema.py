
from drf_yasg import openapi

APIResponseSchema = {
    'status': openapi.Schema(
        type=openapi.TYPE_STRING,
        enum=['success', 'error'],
    ),
    'message': openapi.Schema(type=openapi.TYPE_STRING),
}

APIErrorResponseSchema = APIResponseSchema.copy()
APIErrorResponseSchema['data'] = openapi.Schema(type=openapi.TYPE_OBJECT, x_nullable=True)
APIErrorResponse = openapi.Schema(
    title='API Error Response',
    type=openapi.TYPE_OBJECT,
    properties=APIErrorResponseSchema
)