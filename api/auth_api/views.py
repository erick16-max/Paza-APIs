from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

from  api.serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
def get_auth_apis(request):
    routes = [
        'api-auth/tokens/',
        'api-auth/token/refresh/',
        'api-auth/signup/'
    ]

    return Response(routes)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer