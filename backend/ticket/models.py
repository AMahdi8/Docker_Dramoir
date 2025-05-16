from django.db import models
from django.utils.translation import gettext_lazy as _

class Ticket(models.Model):
    """مدل تیکت‌های پشتیبانی"""
    
    STATUS_CHOICES = (
        ('pending', _('در انتظار بررسی')),
        ('in_progress', _('در حال بررسی')),
        ('resolved', _('حل شده')),
        ('closed', _('بسته شده')),
    )
    
    PRIORITY_CHOICES = (
        ('low', _('کم')),
        ('medium', _('متوسط')),
        ('high', _('زیاد')),
        ('urgent', _('فوری')),
    )
    
    subject = models.CharField(_('موضوع'), max_length=255)
    description = models.TextField(_('توضیحات'))
    name = models.CharField(_('نام'), max_length=100)
    email = models.EmailField(_('ایمیل'))
    phone = models.CharField(_('شماره تماس'), max_length=20, blank=True, null=True)
    status = models.CharField(_('وضعیت'), max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(_('اولویت'), max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاریخ بروزرسانی'), auto_now=True)
    
    class Meta:
        verbose_name = _('تیکت')
        verbose_name_plural = _('تیکت‌ها')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.name}"
    
class TicketReply(models.Model):
    """مدل پاسخ‌های تیکت"""
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies', verbose_name=_('تیکت'))
    message = models.TextField(_('پیام'))
    is_staff_reply = models.BooleanField(_('پاسخ پشتیبانی'), default=False)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('پاسخ تیکت')
        verbose_name_plural = _('پاسخ‌های تیکت')
        ordering = ['created_at']
    
    def __str__(self):
        return f"پاسخ به {self.ticket.subject}"

class Request(models.Model):
    """مدل درخواست‌های کاربران"""
    
    STATUS_CHOICES = (
        ('pending', _('در انتظار بررسی')),
        ('approved', _('تایید شده')),
        ('rejected', _('رد شده')),
    )
    
    TYPE_CHOICES = (
        ('movie', _('فیلم')),
        ('series', _('سریال')),
        ('subtitle', _('زیرنویس')),
        ('other', _('سایر')),
    )
    
    title = models.CharField(_('عنوان'), max_length=255)
    description = models.TextField(_('توضیحات'), blank=True, null=True)
    type = models.CharField(_('نوع'), max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(_('نام'), max_length=100)
    email = models.EmailField(_('ایمیل'))
    status = models.CharField(_('وضعیت'), max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاریخ بروزرسانی'), auto_now=True)
    
    class Meta:
        verbose_name = _('درخواست')
        verbose_name_plural = _('درخواست‌ها')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_type_display()} - {self.name}"
