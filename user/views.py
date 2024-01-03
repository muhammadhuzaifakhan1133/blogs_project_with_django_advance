from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import UserRegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

class RegisterAPIView(APIView):
    def post(self, request: Request):
        serialized_data = UserRegisterSerializer(data=request.data)
        # if (request.data.get("password") != request.data.get("confirm_password")):
        #     return Response({
        #         "error": "Password and Confirm Password does not match"
        #     })
        if serialized_data.is_valid():
            user: User = serialized_data.save()
            user.set_password(request.data['password'])
            user.is_staff = "1"
            user.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({
                "error": "Please enter username and password"
            }, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({
                "error": "User does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
        is_valid_user = authenticate(username=username, password=password)
        if is_valid_user is None:
            return Response({
                "error": "wrong credentials"
            })
        login(user=user, request=request)
        return Response({
            "message": "user loggedin successfully"
        })