from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Note

# PUBLIC_INTERFACE
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration endpoint.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', "password2", "email", "first_name", "last_name")
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"]
        )
        return user

# PUBLIC_INTERFACE
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login endpoint.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

# PUBLIC_INTERFACE
class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for CRUD operations on Note model.
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "updated_at", "user"]
