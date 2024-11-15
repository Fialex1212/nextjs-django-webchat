from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
        
    def create(self, validate_data):
        user = CustomUser(
            email = validate_data['email'],
            username = validate_data['username']
        )
        user.set_password(validate_data['password'])
        user.save()
        return user
    
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class UserUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }
        
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        password = validate_password.get('password')
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['id'] = str(user.id)
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add additional user information to the response
        data['user'] = UserSerializers(self.user).data
        return data
