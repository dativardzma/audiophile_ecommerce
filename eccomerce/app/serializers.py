from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    repeate_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'repeate_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['repeate_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
        
    # def create(self, validated_data):
    #     validated_data.pop('repeate_password')  # Remove repeat_password before creating user
    #     user = User(
    #         username=validated_data['username'],
    #         email=validated_data['email']
    #     )
    #     user.set_password(validated_data['password'])  # Hash the password
    #     user.save()
    #     return user

    def get_token(self, user):
        token = RefreshToken.for_user(user)
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }