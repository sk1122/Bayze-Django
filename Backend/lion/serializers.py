from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['email', 'password']
		extra_kwargs = {'password': {'write_only': True}}

	def validate_password(self, attrs):
		password = attrs

		if len(password) < 8:
			raise serializers.ValidationError('Password Must be 8 Chars Long')

		return attrs

	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		return user


class UserLoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=200)
	password = serializers.CharField(max_length=200, write_only=True)
	refresh_token = serializers.CharField(max_length=255, read_only=True)
	access_token = serializers.CharField(max_length=255, read_only=True)

	def validate(self, data):
		data_lst = list(data.items())
		email = data_lst[0][1]
		password = data_lst[1][1]

		user = authenticate(email=email, password=password)
		
		if user is None:
			raise serializers.ValidationError('A user with this email and password is not found.')

		try:
			update_last_login(None, user)
		except User.DoesNotExist:
			raise serializers.ValidationError(
				'User with given email and password does not exists'
			)
			
		refresh = RefreshToken.for_user(user)

		return {
	        'refresh_token': str(refresh),
	        'access_token': str(refresh.access_token),
			'email': user.email
	    }
