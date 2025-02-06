from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import (UserSerializer, UserCreateSerializer, UserLoginSerializer,
                          UserChangePasswordSerializer, UserResetPasswordSerializer, UserResetPasswordConfirmSerializer)
from .models import User
from .utils import send_password_reset_email


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh.access_token),
        'access': str(refresh.access_token),
    }

class UserCreateView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token':token}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token = get_tokens_for_user(user)
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserPofileView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Password Changed Successfully.'}, status=status.HTTP_200_OK)


class UserResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        serializer = UserResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=email)
        # force_bytes converts user_id into bytes and urlsafe_base64_encode
        # encode a bytestring to a base64 string for use in URLs.
        uid = urlsafe_base64_encode(force_bytes(user.id))
        # Generate token for password reset mechanism
        token = default_token_generator.make_token(user)
        # Generate link by combining url+uid+token
        link = f'http://localhost:3000/auth/user/reset_password_confirm/?uid={uid}&token={token}'
        # send email (reset link) TODO
        data = {
            "subject": "Reset Your Password",
            "body": f"Click following link to reset your password: {link}",
            "to_email": "syedyousafshah0.98@gmail.com"
        }
        send_password_reset_email(data)
        return Response({'msg': f'Password reset link send.Please check your Email<{user.email}>.'},
                        status=status.HTTP_200_OK)


class UserResetPasswordConfirmView(APIView):
    def post(self, request):
        uid = request.query_params.get('uid')
        token = request.query_params.get('token')
        user_id = smart_str(urlsafe_base64_decode(uid))
        try:
            user = User.objects.filter(pk=user_id).first()
            is_token_valid = default_token_generator.check_token(user=user, token=token)
            if not (user and is_token_valid):
                return Response({'error': 'Token is Invalid or Expired.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = UserResetPasswordConfirmSerializer(data=request.data, context={'user': user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'msg': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token is Invalid or Expired.'}, status=status.HTTP_400_BAD_REQUEST)
