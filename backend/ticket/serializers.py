from rest_framework import serializers
from .models import Ticket, TicketReply, Request

class TicketReplySerializer(serializers.ModelSerializer):
    """سریالایزر برای پاسخ‌های تیکت - فقط برای نمایش"""
    class Meta:
        model = TicketReply
        fields = ['id', 'message', 'is_staff_reply', 'created_at']
        read_only_fields = ['is_staff_reply', 'created_at']

class TicketSerializer(serializers.ModelSerializer):
    """سریالایزر برای نمایش تیکت‌ها با پاسخ‌های آنها"""
    replies = TicketReplySerializer(many=True, read_only=True)
    
    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'name', 'email', 'phone', 
                 'status', 'priority', 'created_at', 'updated_at', 'replies']
        read_only_fields = ['status', 'priority', 'created_at', 'updated_at']

class TicketCreateSerializer(serializers.ModelSerializer):
    """سریالایزر برای ایجاد تیکت جدید"""
    class Meta:
        model = Ticket
        fields = ['subject', 'description', 'name', 'email', 'phone']

class TicketReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReply
        fields = ['ticket', 'message']

class RequestSerializer(serializers.ModelSerializer):
    """سریالایزر برای نمایش درخواست‌ها"""
    class Meta:
        model = Request
        fields = ['id', 'title', 'description', 'type', 'name', 'email', 
                 'status', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']

class RequestCreateSerializer(serializers.ModelSerializer):
    """سریالایزر برای ایجاد درخواست جدید"""
    class Meta:
        model = Request
        fields = ['title', 'description', 'type', 'name', 'email'] 