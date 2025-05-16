from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import VerificationCode, PasswordResetCode, User, Favorite
import base64
from django.core.files.base import ContentFile
from movie.models import Movie, Series

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class VerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture_base64 = serializers.CharField(write_only=True, required=False)
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_verified', 'profile_picture_url', 'profile_picture_base64']
        read_only_fields = ['id', 'email', 'date_joined', 'is_verified']

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        return None

    def update(self, instance, validated_data):
        # Update user profile fields
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        profile_picture_base64 = validated_data.pop('profile_picture_base64', None)
        
        if profile_picture_base64:
            try:
                # Remove header if present and get format
                if ';base64,' in profile_picture_base64:
                    header, base64_data = profile_picture_base64.split(';base64,')
                    # Extract format from header (e.g., "data:image/jpeg" -> "jpeg")
                    image_format = header.split('/')[-1].lower()
                else:
                    base64_data = profile_picture_base64
                    image_format = 'jpeg'  # Default to jpeg if no header

                # Validate format
                if image_format not in ['jpeg', 'jpg', 'png']:
                    raise serializers.ValidationError({'profile_picture_base64': 'Invalid image format. Only JPEG and PNG are allowed.'})

                # Convert base64 to file
                image_data = base64.b64decode(base64_data)
                
                # Use jpg extension for jpeg format
                if image_format == 'jpeg':
                    image_format = 'jpg'
                
                filename = f'profile_picture_{instance.id}.{image_format}'
                instance.profile_picture.save(filename, ContentFile(image_data), save=False)
            except Exception as e:
                raise serializers.ValidationError({'profile_picture_base64': 'Invalid base64 image data'})

        return super().update(instance, validated_data)

class FavoriteSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    poster_path = serializers.CharField(read_only=True)
    overview = serializers.CharField(read_only=True)
    vote_average = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'content_id', 'content_type', 'added_at', 'title', 'poster_path', 'overview', 'vote_average']
        read_only_fields = ['added_at', 'title', 'poster_path', 'overview', 'vote_average']

    def validate(self, data):
        content_id = data.get('content_id')
        content_type = data.get('content_type')
        
        if content_type not in ['movie', 'series']:
            raise serializers.ValidationError({"content_type": "Content type must be either 'movie' or 'series'"})
        
        # Check if content exists
        if content_type == 'movie':
            content = Movie.objects.filter(id=content_id).first()
        else:
            content = Series.objects.filter(id=content_id).first()
            
        if not content:
            raise serializers.ValidationError({"content_id": f"{content_type.capitalize()} with this ID does not exist"})
            
        return data

    def create(self, validated_data):
        content_id = validated_data['content_id']
        content_type = validated_data['content_type']
        user = validated_data['user']
        
        # Check if already in favorites
        existing = Favorite.objects.filter(user=user, content_id=content_id, content_type=content_type).first()
        if existing:
            return existing
        
        # Get content data based on type
        if content_type == 'movie':
            content = Movie.objects.get(id=content_id)
            title = content.title
            poster_path = content.image.url if content.image else None
            overview = content.description
            vote_average = float(content.rate) if content.rate else 0
        else:
            content = Series.objects.get(id=content_id)
            title = content.title
            poster_path = content.image.url if content.image else None
            overview = content.description
            vote_average = float(content.rate) if content.rate else 0
        
        # Create favorite with content data
        favorite = Favorite.objects.create(
            user=user,
            content_id=content_id,
            content_type=content_type,
            title=title,
            poster_path=poster_path,
            overview=overview,
            vote_average=vote_average
        )
        
        return favorite 