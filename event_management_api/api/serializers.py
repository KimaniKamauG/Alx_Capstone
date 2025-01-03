from rest_framework import serializers 
from events.models import Event, Category
from django.utils import timezone
from django.contrib.auth import get_user_model



from django.contrib.auth.password_validation import validate_password


User = get_user_model() 


class UserSerializer(serializers.ModelSerializer):
    '''
    Serializer for the User Model

    Handles user registration and profile updates.
    '''
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User 
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user 
    
# The one below was before i came up with better ideas.
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User 
#         fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    '''Serializer for the Event Category Model'''
    class Meta:
        model = Category 
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Event Model
    
    Handles event creation, updates and detailed view.
    '''
    organizer = UserSerializer(read_only=True)
    attendees = UserSerializer(read_only=True, many=True)
    is_full = serializers.BooleanField(read_only=True)
    class Meta:
        model = Event 
        fields = '__all__'
        read_only_fields = ['created_at', 'organizer', 'attendees']

    def validate_date_time(self, value):
        '''
        Validate that event date is not in the past.
        '''
        if value < timezone.now():
            raise serializers.ValidationError('Event date cannot be in the past.')
        return value
    def get_attendee_count(self, obj):
        '''
        Get the current number of attendees.
        '''
        return obj.attendees.count()

