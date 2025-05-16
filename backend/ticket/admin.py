from django.contrib import admin
from django.utils.html import format_html
from .models import Ticket, TicketReply, Request

class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'status', 'priority', 'created_at', 'updated_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('subject', 'description', 'name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TicketReplyInline]
    fieldsets = (
        ('اطلاعات تیکت', {
            'fields': ('subject', 'description', 'status', 'priority')
        }),
        ('اطلاعات تماس', {
            'fields': ('name', 'email', 'phone')
        }),
        ('تاریخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_in_progress', 'mark_as_resolved', 'mark_as_closed']
    
    @admin.action(description="علامت‌گذاری به عنوان در حال بررسی")
    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
        
    @admin.action(description="علامت‌گذاری به عنوان حل شده")
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved')
        
    @admin.action(description="علامت‌گذاری به عنوان بسته شده")
    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')

@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'is_staff_reply', 'short_message', 'created_at')
    list_filter = ('is_staff_reply', 'created_at')
    search_fields = ('ticket__subject', 'message')
    readonly_fields = ('created_at',)
    
    def short_message(self, obj):
        if len(obj.message) > 100:
            return obj.message[:100] + "..."
        return obj.message
    short_message.short_description = "پیام"

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'name', 'email', 'status', 'created_at')
    list_filter = ('status', 'type', 'created_at')
    search_fields = ('title', 'description', 'name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('اطلاعات درخواست', {
            'fields': ('title', 'description', 'type', 'status')
        }),
        ('اطلاعات تماس', {
            'fields': ('name', 'email')
        }),
        ('تاریخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_approved', 'mark_as_rejected']
    
    @admin.action(description="علامت‌گذاری به عنوان تایید شده")
    def mark_as_approved(self, request, queryset):
        queryset.update(status='approved')
        
    @admin.action(description="علامت‌گذاری به عنوان رد شده")
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
