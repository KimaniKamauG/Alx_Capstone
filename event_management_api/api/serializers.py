from rest_framework import serializers 
from events.models import Event
from django.utils import timezone
from django.contrib.auth import get_user_model



from django.contrib.auth.password_validation import validate_password
#from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate

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
            #token = Token.objects.create(user=user)
        return user 


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



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        attrs['user'] = user
        return attrs
        #raise serializers.ValidationError('Invalid credentials')
    

class TokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        attrs['user'] = user
        return attrs
    

    

# from django.contrib.auth.password_validation import validate_password
# from rest_framework.authtoken.models import Token 

# class DumbUserSerializer(serializers.Serializer):
#     password = serializers.CharField()
#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'email','password']

#     def validate_password(self, value):
#         validate_password(value)
#         return value
    
#     def create(self, validated_data):
#         user = get_user_model().objects.create_user(validated_data)
#         if 'password' in validated_data:
#             user.set_password(validated_data['password'])
#             user.save()
#             token = Token.objects.create(user=user)
#         return user, token