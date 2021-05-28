from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from allauth.socialaccount.models import SocialAccount, SocialToken

from django.shortcuts import render

from .models import *

from .Facebook import FacebookAds, FacebookBusiness

import os
from dotenv import load_dotenv
load_dotenv()

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
	permission_classes = (AllowAny, )
	def get(self, request):
		user = User.objects.filter(email='punekar.satyam@gmail.com').first()
		token = AccessTokens.objects.filter(user=user).first()
		
		graph = facebook.GraphAPI(access_token=token) # GraphAPI is FB's API for Querying
		page_data = graph.get_object('me/accounts?limit=99') # Get data from https://graph.facebook.com/me/accounts
		data = {
			'access_token': token,
		}
		resp = graph.get_object('me/accounts?after={0}'.format(page_data['paging']['cursors']['after']))
		print(resp)
		print(page_data)

		for page in page_data.get('data', {}):
			page_id = page["id"]
			page_name = page["name"]
			category = page["category_list"]

			# Check if Page already exists
			page_data = FacebookPages.objects.filter(page_id=page_id).first()

			if page_data is None:
				page_data = FacebookPages.objects.create(user=user, page_id=page_id, page=page_name, category=category)
			else:
				page_data.page_id = page_id
				page_data.page = page_name
				page_data.category = category
		return Response({"data": "data"})


class Campaign(APIView):
	permission_classes = (IsAuthenticated, )

	def get(self, request):
		token = AccessTokens.objects.filter(user=request.user).first()
		
		ad_account_id = 'act_203132874856467'
		app_secret = os.environ.get('FACEBOOK_SECRET')
		app_id = os.environ.get('FACEBOOK_CLIENT_ID')
		page_id = '135223993953004'

		campaign = FacebookAds(token.token, ad_account_id, app_secret, page_id, app_id)

		fields = [
		]
		params = {
		    'name': 'My Campaign',
		    'buying_type': 'AUCTION',
		    'objective': 'PAGE_LIKES',
		    'status': 'PAUSED',
		    'special_ad_categories': []
		}

		campaign_id = campaign.create_campaign(fields, params).get_id()
		print('campaign_id:', campaign_id, '\n')

		fields = [
		]
		params = {
			'name': 'My AdSet',
			'optimization_goal': 'PAGE_LIKES',
			'billing_event': 'IMPRESSIONS',
			'bid_amount': '20',
			'promoted_object': {'page_id': page_id},
			'daily_budget': 10000,
			'campaign_id': campaign_id,
			'targeting': {'geo_locations':{'countries':['US']}},
			'status': 'PAUSED',
		}
		ad_set_id = campaign.create_ad_set(fields, params).get_id()
		print('ad_set_id:', ad_set_id, '\n')

		fields = [
		]
		params = {
			'name': 'My Creative',
			'object_id': page_id,
			'title': 'My Page Like Ad',
			'body': 'Like My Page',
			'image_url': '',
		}
		creative_id = campaign.create_creative()
		print('creative_id:', creative_id, '\n')

		fields = [
		]
		params = {
			'name': 'My Ad',
			'adset_id': ad_set_id,
		    'creative': {'creative_id':creative_id},
			'status': 'PAUSED',
		}
		ad_id = campaign.create_ad(fields, params).get_id()
		print('ad_id:', ad_id, '\n')
		
		fields = [
		]
		params = {
			'ad_format': 'DESKTOP_FEED_STANDARD',
		}
		print(campaign.ad_preview(ad_id, fields, params))

		return Response({"data": campaign_id})


class BusinessUsers(APIView):
	permission_classes = (IsAuthenticated, )

	def get(self, request):
		token = AccessTokens.objects.filter(user=request.user).first().token
		user_id = SocialAccount.objects.filter(user=request.user, provider='facebook').first().uid
		print(user_id)
		facebook = FacebookBusiness(user_id, token)

		facebook.get_business_users()
		facebook.get_business_ad_accounts()
		facebook.get_personal_ad_accounts()
		facebook.check_tos_accepted()

		return Response({'done': True})