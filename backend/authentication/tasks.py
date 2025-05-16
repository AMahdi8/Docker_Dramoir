from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

# Get logger
logger = logging.getLogger('celery')

@shared_task(bind=True, max_retries=3)
def send_verification_email(self, email, verification_code):
    """
    Send verification email with the provided code.
    """
    logger.info(f"Sending verification email to {email} with code {verification_code}")
    
    subject = 'Email Verification Code'
    message = f'Your verification code is: {verification_code}. This code will expire in 15 minutes.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        logger.info(f"Verification email sent successfully to {email}")
        return f"Verification email sent to {email}"
    except Exception as exc:
        logger.error(f"Failed to send verification email to {email}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_password_reset_email(self, email, reset_code):
    """
    Send password reset email with the provided code.
    """
    logger.info(f"Sending password reset email to {email} with code {reset_code}")
    
    subject = 'Password Reset Code'
    message = f'Your password reset code is: {reset_code}. This code will expire in 15 minutes.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        logger.info(f"Password reset email sent successfully to {email}")
        return f"Password reset email sent to {email}"
    except Exception as exc:
        logger.error(f"Failed to send password reset email to {email}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60) 