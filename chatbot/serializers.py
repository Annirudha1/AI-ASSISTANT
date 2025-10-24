from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Chat

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class ChatSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Chat
        fields = ('id', 'user', 'question', 'answer', 'timestamp')
        read_only_fields = ('user', 'answer', 'timestamp')







