from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

from .models import User, VerificationCode, PasswordResetCode
from .serializers import (
    UserRegistrationSerializer,
    VerificationCodeSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from .tasks import send_verification_email, send_password_reset_email

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate verification code
        code = VerificationCode.generate_code()
        expires_at = timezone.now() + timedelta(minutes=15)
        VerificationCode.objects.create(
            user=user,
            code=code,
            expires_at=expires_at
        )

        # Send verification email using Celery task
        send_verification_email.delay(user.email, code)

        return Response({
            'message': 'User registered successfully. Please check your email for verification code.',
            'email': user.email
        }, status=status.HTTP_201_CREATED)

class VerifyEmailView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerificationCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(email=email)
            verification_code = VerificationCode.objects.filter(
                user=user,
                code=code,
                is_used=False
            ).latest('created_at')

            if not verification_code.is_valid():
                return Response(
                    {'error': 'Invalid or expired code'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.is_verified = True
            user.save()
            verification_code.mark_as_used()

            return Response({
                'message': 'Email verified successfully'
            }, status=status.HTTP_200_OK)

        except (User.DoesNotExist, VerificationCode.DoesNotExist):
            return Response(
                {'error': 'Invalid email or code'},
                status=status.HTTP_400_BAD_REQUEST
            )

class LoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not user.is_verified:
                return Response(
                    {'error': 'Email not verified'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username
                }
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )

class PasswordResetRequestView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            code = PasswordResetCode.generate_code()
            expires_at = timezone.now() + timedelta(minutes=15)
            PasswordResetCode.objects.create(
                user=user,
                code=code,
                expires_at=expires_at
            )

            # Send password reset email using Celery task
            send_password_reset_email.delay(user.email, code)

            return Response({
                'message': 'Password reset code sent to your email',
                'email': user.email
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

class PasswordResetConfirmView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(email=email)
            reset_code = PasswordResetCode.objects.filter(
                user=user,
                code=code,
                is_used=False
            ).latest('created_at')

            if not reset_code.is_valid():
                return Response(
                    {'error': 'Invalid or expired code'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()
            reset_code.mark_as_used()

            return Response({
                'message': 'Password reset successfully'
            }, status=status.HTTP_200_OK)

        except (User.DoesNotExist, PasswordResetCode.DoesNotExist):
            return Response(
                {'error': 'Invalid email or code'},
                status=status.HTTP_400_BAD_REQUEST
            ) 