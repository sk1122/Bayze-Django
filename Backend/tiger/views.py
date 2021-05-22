from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from allauth.socialaccount.models import SocialAccount, SocialToken

from django.shortcuts import render

from .models import *

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

class Profile(APIView):
	'''
		Profile is used to show Profile Data of Logged In User
	'''

	permission_classes = (IsAuthenticated, )
	def get(self, request):
		data = SocialAccount.objects.filter(user=request.user).first()
		name = data.extra_data["first_name"] + data.extra_data["last_name"]
		page_data = FacebookPages.objects.filter(user=request.user)

		context = {
			'user': request.user,
			'name': name,
			'pages': page_data
		}

		return render(request, "registration/profile.html", context)

class Demo(APIView):
	permission_classes = (IsAuthenticated, )
	def get(self, request):
		token = AccessTokens.objects.filter(user=request.user).first()
		
		# my_app_id = '4118143361578217'
		# my_app_secret = 'cfa0eab1d7e579e74f3f87aaf89ed774'

		# FacebookAdsApi.init(my_app_id, my_app_secret, token.token)
		# my_account = AdAccount('act_3424')
		# campaigns = my_account.get_campaigns()
		# print(campaigns)
		return Response({"data": "data"})