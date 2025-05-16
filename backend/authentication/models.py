from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, verbose_name='عکس پروفایل')

    # اضافه کردن related_name برای جلوگیری از تداخل با مدل کاربر پیش‌فرض
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='authentication_user_set',
        related_query_name='authentication_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='authentication_user_set',
        related_query_name='authentication_user'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.code}"

    @classmethod
    def generate_code(cls, user=None):
        import random
        import string
        
        # If called without user, just return the code
        if user is None:
            return ''.join(random.choices(string.digits, k=6))
            
        # If called with user, create and return the instance
        from datetime import datetime, timedelta
        
        code = ''.join(random.choices(string.digits, k=6))
        expires_at = datetime.now() + timedelta(minutes=15)
        
        return cls.objects.create(
            user=user,
            code=code,
            expires_at=expires_at
        )

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()

    def mark_as_used(self):
        self.is_used = True
        self.save()

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.code}"

    @classmethod
    def generate_code(cls, user=None):
        import random
        import string
        
        # If called without user, just return the code
        if user is None:
            return ''.join(random.choices(string.digits, k=6))
            
        # If called with user, create and return the instance
        from datetime import datetime, timedelta
        
        code = ''.join(random.choices(string.digits, k=6))
        expires_at = datetime.now() + timedelta(minutes=15)
        
        return cls.objects.create(
            user=user,
            code=code,
            expires_at=expires_at
        )

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()

    def mark_as_used(self):
        self.is_used = True
        self.save()

class Favorite(models.Model):
    CONTENT_TYPES = (
        ('movie', 'Movie'),
        ('series', 'Series'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    content_id = models.IntegerField()  # TMDB ID of movie or series
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    added_at = models.DateTimeField(auto_now_add=True)
    
    # Content data fields
    title = models.CharField(max_length=255, null=True, blank=True)
    poster_path = models.URLField(max_length=500, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    vote_average = models.FloatField(default=0)

    class Meta:
        # Ensure a user can't add the same content twice
        unique_together = ('user', 'content_id', 'content_type')
        ordering = ['-added_at']  # Latest favorites first 