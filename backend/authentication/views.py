from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import VerificationCode, PasswordResetCode, Favorite
from .serializers import (
    UserRegistrationSerializer,
    VerificationCodeSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UserProfileSerializer,
    FavoriteSerializer
)
import random
import string
from datetime import timedelta
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .tasks import send_verification_email, send_password_reset_email
from rest_framework.permissions import AllowAny
import logging

User = get_user_model()

logger = logging.getLogger('django')

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

        # Send verification email asynchronously
        send_verification_email.delay(user.email, code)

        return Response({
            'message': 'User registered successfully. Please check your email for verification code.',
            'email': user.email
        }, status=status.HTTP_201_CREATED)

class VerifyEmailView(APIView):
    @swagger_auto_schema(
        operation_description="تایید ایمیل با کد ارسال شده - نیاز به هدر خاصی ندارد",
        request_body=VerificationCodeSerializer,
        responses={200: openapi.Response('ایمیل با موفقیت تایید شد')}
    )
    def post(self, request):
        serializer = VerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            
            try:
                user = User.objects.get(email=email)
                verification = VerificationCode.objects.get(
                    user=user,
                    code=code,
                    is_used=False,
                    expires_at__gt=timezone.now()
                )
                
                user.is_verified = True
                user.save()
                
                verification.is_used = True
                verification.save()
                
                return Response(
                    {'message': 'Email verified successfully'},
                    status=status.HTTP_200_OK
                )
            except (User.DoesNotExist, VerificationCode.DoesNotExist):
                return Response(
                    {'error': 'Invalid verification code'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="ورود کاربر و دریافت توکن - نیاز به هدر خاصی ندارد",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="ورود موفق - توکن‌های دسترسی و رفرش برگردانده می‌شوند",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='توکن دسترسی JWT'),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='توکن رفرش JWT'),
                    }
                )
            )
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(email=email)
                if not user.is_verified:
                    return Response(
                        {'error': 'Please verify your email first'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if user.check_password(password):
                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(user)
                    
                    return Response({
                        'access': str(refresh.access_token),
                        'refresh': str(refresh)
                    }, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'error': 'Invalid credentials'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

            # Debug direct email sending
            logger.info(f"DEBUG: Attempting direct email send to {email}")
            try:
                # Try sending email directly (not through Celery)
                send_mail(
                    'Password Reset Code (Direct)',
                    f'Your direct password reset code is: {code}. This code will expire in 15 minutes.',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                logger.info(f"DEBUG: Direct email send succeeded to {email}")
            except Exception as e:
                logger.error(f"DEBUG: Direct email send failed to {email}: {str(e)}")

            # Send through Celery task as usual
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

class PasswordResetConfirmView(APIView):
    @swagger_auto_schema(
        operation_description="تایید و تغییر رمز عبور با کد دریافتی - نیاز به هدر خاصی ندارد",
        request_body=PasswordResetConfirmSerializer,
        responses={200: openapi.Response('رمز عبور با موفقیت تغییر کرد')}
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = User.objects.get(email=email)
                reset_code = PasswordResetCode.objects.get(
                    user=user,
                    code=code,
                    is_used=False,
                    expires_at__gt=timezone.now()
                )
                
                user.set_password(new_password)
                user.save()
                
                reset_code.is_used = True
                reset_code.save()
                
                return Response(
                    {'message': 'Password reset successful'},
                    status=status.HTTP_200_OK
                )
            except (User.DoesNotExist, PasswordResetCode.DoesNotExist):
                return Response(
                    {'error': 'Invalid reset code'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""دریافت و ویرایش پروفایل کاربر
        هدرهای مورد نیاز:
        Authorization: Bearer {توکن_دسترسی}""",
        responses={200: UserProfileSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="""ویرایش پروفایل کاربر
        هدرهای مورد نیاز:
        Authorization: Bearer {توکن_دسترسی}
        Content-Type: application/json""",
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""دریافت لیست علاقه‌مندی‌های کاربر
        هدرهای مورد نیاز:
        Authorization: Bearer {توکن_دسترسی}""",
        responses={200: FavoriteSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="""افزودن فیلم یا سریال به علاقه‌مندی‌ها - نیاز به آیدی محتوا و نوع آن (فیلم یا سریال) دارد
        هدرهای مورد نیاز:
        Authorization: Bearer {توکن_دسترسی}
        Content-Type: application/json""",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['content_id', 'content_type'],
            properties={
                'content_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='شناسه فیلم یا سریال'),
                'content_type': openapi.Schema(type=openapi.TYPE_STRING, description='نوع محتوا', enum=['movie', 'series'])
            }
        ),
        responses={201: FavoriteSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteDeleteView(generics.DestroyAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'content_id'

    @swagger_auto_schema(
        operation_description="""حذف فیلم یا سریال از علاقه‌مندی‌ها - نیاز به آیدی محتوا و نوع آن دارد
        هدرهای مورد نیاز:
        Authorization: Bearer {توکن_دسترسی}
        
        پارامترهای URL:
        content_id: شناسه محتوا
        type: نوع محتوا (movie یا series)""",
        manual_parameters=[
            openapi.Parameter(
                'type',
                openapi.IN_QUERY,
                description='نوع محتوا (movie یا series)',
                type=openapi.TYPE_STRING,
                required=True,
                enum=['movie', 'series']
            )
        ],
        responses={
            204: openapi.Response('محتوا با موفقیت از علاقه‌مندی‌ها حذف شد'),
            404: openapi.Response('محتوا در لیست علاقه‌مندی‌ها یافت نشد')
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        content_type = self.request.query_params.get('type')
        if not content_type or content_type not in ['movie', 'series']:
            raise ValidationError({"type": "Content type must be either 'movie' or 'series'"})
            
        return Favorite.objects.filter(
            user=self.request.user,
            content_type=content_type
        )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response(
                {"detail": "This content is not in your favorites."},
                status=status.HTTP_404_NOT_FOUND
            ) 