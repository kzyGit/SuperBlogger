from rest_framework import generics, status
from ..serializers import (UserSerializer, TokenSerializer)
from ..models import User
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny,)
from ..permissions import IsAdminUserOrReadOnly
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly, )


class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = TokenSerializer(data={
                "token": jwt_encode_handler(jwt_payload_handler(user))})
            serializer.is_valid()
            data = {
                'message': 'successful login',
                'token': serializer.data['token']
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': 'Invalid credentials'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        logout(request)
        return Response({'message': 'successful logout'},
                        status=status.HTTP_200_OK)
