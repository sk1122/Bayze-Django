from django.contrib.auth import login, authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from .models import *

from allauth.socialaccount.models import SocialAccount

class RegistrationView(APIView):
	'''
		It is used for Register View
	'''

	serializer_class = UserRegistrationSerializer
	permission_classes = (AllowAny, )

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			serializer.save()
			status_code = status.HTTP_201_CREATED
			response = {
				'success': 'True',
				'status': status_code,
				'message': 'User Created Successfully'
			}

			return Response(response, status=status_code)
		return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
	'''
		Login
	'''

	permission_classes = (AllowAny, )

	def post(self, request):
		email = request.data.get('email')
		password = request.data.get('password')

		user = authenticate(email=email, password=password)

		if user is None:
			return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

		update_last_login(None, user)
		login(request, user)

		refresh = RefreshToken.for_user(user)
		data = {
		    'refresh_token': str(refresh),
		    'access_token': str(refresh.access_token),
			'email': user.email
		}

		return Response({"data": data}, status=status.HTTP_200_OK)