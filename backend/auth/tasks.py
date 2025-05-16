from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_verification_email(email, verification_code):
    """
    Send verification email with the provided code.
    """
    subject = 'Email Verification Code'
    message = f'Your verification code is: {verification_code}. This code will expire in 15 minutes.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
    
    return f"Verification email sent to {email}"


@shared_task
def send_password_reset_email(email, reset_code):
    """
    Send password reset email with the provided code.
    """
    subject = 'Password Reset Code'
    message = f'Your password reset code is: {reset_code}. This code will expire in 15 minutes.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
    
    return f"Password reset email sent to {email}" 