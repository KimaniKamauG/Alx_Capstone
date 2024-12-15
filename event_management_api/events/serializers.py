from rest_framework import serializers 
from .models import Event, Participant
#from users.models import CustomUser 
from django.contrib.auth import get_user_model

User = get_user_model() 

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event 
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant 
        fields = ['id', 'name', 'email']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user 



