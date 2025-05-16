from django.shortcuts import render
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Ticket, TicketReply, Request
from .serializers import (
    TicketSerializer, TicketCreateSerializer, 
    TicketReplySerializer, TicketReplyCreateSerializer,
    RequestSerializer, RequestCreateSerializer
)

# Create your views here.

class TicketViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """سیستم تیکت‌های پشتیبانی"""
    
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """فقط تیکت‌های مربوط به کاربر را نمایش می‌دهد"""
        queryset = Ticket.objects.all()
        email = self.request.query_params.get('email', None)
        if email:
            queryset = queryset.filter(email=email)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer
        return TicketSerializer
    
    @swagger_auto_schema(
        operation_description="ثبت تیکت جدید",
        request_body=TicketCreateSerializer,
        responses={201: TicketSerializer}
    )
    def create(self, request, *args, **kwargs):
        """ثبت تیکت جدید"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="حذف تیکت",
        responses={204: "تیکت با موفقیت حذف شد"}
    )
    def destroy(self, request, *args, **kwargs):
        """حذف تیکت"""
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="لیست تیکت‌ها",
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_QUERY, description="فیلتر بر اساس ایمیل", type=openapi.TYPE_STRING)
        ]
    )
    def list(self, request, *args, **kwargs):
        """لیست تیکت‌ها"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="مشاهده جزئیات تیکت"
    )
    def retrieve(self, request, *args, **kwargs):
        """مشاهده جزئیات تیکت"""
        return super().retrieve(request, *args, **kwargs)

class RequestViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """سیستم درخواست‌های کاربران"""
    
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """فقط درخواست‌های مربوط به کاربر را نمایش می‌دهد"""
        queryset = Request.objects.all()
        email = self.request.query_params.get('email', None)
        if email:
            queryset = queryset.filter(email=email)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RequestCreateSerializer
        return RequestSerializer
    
    @swagger_auto_schema(
        operation_description="ثبت درخواست جدید",
        request_body=RequestCreateSerializer,
        responses={201: RequestSerializer}
    )
    def create(self, request, *args, **kwargs):
        """ثبت درخواست جدید"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="حذف درخواست",
        responses={204: "درخواست با موفقیت حذف شد"}
    )
    def destroy(self, request, *args, **kwargs):
        """حذف درخواست"""
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="لیست درخواست‌ها",
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_QUERY, description="فیلتر بر اساس ایمیل", type=openapi.TYPE_STRING)
        ]
    )
    def list(self, request, *args, **kwargs):
        """لیست درخواست‌ها"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="مشاهده جزئیات درخواست"
    )
    def retrieve(self, request, *args, **kwargs):
        """مشاهده جزئیات درخواست"""
        return super().retrieve(request, *args, **kwargs)
