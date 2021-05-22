from rest_framework import serializers
from .models import *

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