from rest_framework import serializers 
from events.models import Event, Participant
#from users.models import CustomUser 
from django.contrib.auth import get_user_model



from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate

User = get_user_model() 

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event 
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant 
        fields = [ 'name', 'email']

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    class Meta:
        model = User 
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
            token = Token.objects.create(user=user)
        return user 




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