from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from bar_app.serializers import UserSerializer

class RegisterUser(generics.CreateAPIView):
    """
    Register a new user.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"detail": "User created successfully."},
                status=status.HTTP_201_CREATED
            )

class LoginUser(generics.CreateAPIView):
    """
    Log in a user and return an authentication token.
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            raise NotFound({"detail": "Wrong username or password."})
        token = Token.objects.get_or_create(user=user)
        return Response({"token": token[0].key, "user_id": user.id}, status=status.HTTP_200_OK)

class LogoutUser(generics.CreateAPIView):
    """
    Log out a user by invalidating their authentication token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"detail": "User logged out successfully."})
