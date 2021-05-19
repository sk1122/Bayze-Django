from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from .models import *


class RegistrationView(APIView):
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
	serializer_class = UserLoginSerializer
	permission_classes = (AllowAny, )

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			status_code = status.HTTP_200_OK
			response = {
				'success': 'True',
				'status': status_code,
				'message': 'Login Successfully',
				'data': serializer.data
			}

			return Response(response, status=status_code)
		return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class Demo(APIView):
	permission_classes = (IsAuthenticated, )
	def get(self, request):
		print(request.user)
		return Response({"data": "das"})