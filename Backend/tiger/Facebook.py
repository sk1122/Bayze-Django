import requests
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adpreview import AdPreview
from facebook_business.api import FacebookAdsApi

class FacebookAds:
	def __init__(self, access_token, ad_account_id, app_secret, page_id, app_id):
		self.access_token = access_token
		self.ad_account_id = ad_account_id
		self.app_secret = app_secret
		self.page_id = page_id
		self.app_id = app_id

		FacebookAdsApi.init(access_token=access_token)

	def create_campaign(self, fields, params):
		campaign = AdAccount(self.ad_account_id).create_campaign(
			fields=fields,
			params=params,
		)

		return campaign

	def create_ad_set(self, fields, params):
		ad_set = AdAccount(self.ad_account_id).create_ad_set(
			fields=fields,
			params=params,
		)

		return ad_set

	def create_creative(self):
		# from facebook_business.adobjects.adcreative import AdCreative
		# from facebook_business.adobjects.adcreativelinkdata import AdCreativeLinkData
		# from facebook_business.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec

		# link_data = AdCreativeLinkData()
		# link_data[AdCreativeLinkData.Field.message] = 'try it out'
		# link_data[AdCreativeLinkData.Field.link] = 'https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg'
		# link_data[AdCreativeLinkData.Field.image_hash] = '0c81beadf3af4cd0724dee320ec2a4ee'

		# object_story_spec = AdCreativeObjectStorySpec()
		# object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = self.page_id
		# object_story_spec[AdCreativeObjectStorySpec.Field.link_data] = link_data

		# creative = AdCreative(parent_id=self.ad_account_id)
		# creative['title'] = "My Creative"
		# creative['body'] = "This is my creative's body"
		# creative['object_story_spec'] = object_story_spec
		# creative.remote_create()

		import json
		data = json.dumps({
			'name': 'My Creative',
			'object_id': self.page_id,
			'title': 'My Page Like Ad',
			'body': 'Like My Page',
			'image_url': '',
			'access_token': self.access_token
		})

		creative = requests.post(f'https://graph.facebook.com/v10.0/{self.ad_account_id}/adcreatives', data)

		return creative.json()

	def create_ad(self, fields, params):
		ad = AdAccount(self.ad_account_id).create_ad(
			fields=fields,
			params=params,
		)

		return ad

	def ad_preview(self, ad_id, fields, params):
		return Ad(ad_id).get_previews(
			fields=fields,
			params=params,
		)


class FacebookBusiness:
	def __init__(self, user_id, token):
		self.businessURL = f"https://graph.facebook.com/v10.0/{user_id}/businesses?access_token={token}"

		self.token = token
		self.business_id = ''
		self.personal_id = ''
	
	def get_business_users(self):
		response = requests.get(self.businessURL)
		response = response.json()

		self.business_id = response['data'][0]['id']

	def get_business_ad_accounts(self):
		url = f"https://graph.facebook.com/v10.0/{self.business_id}/owned_ad_accounts?transport=cors&access_token={self.token}"
		response = requests.get(url)
		response = response.json()
		print(response)

	def get_personal_ad_accounts(self):
		personalURL = f"https://graph.facebook.com/v10.0/me/adaccounts?access_token={self.token}&fields=name,id"
		response = requests.get(personalURL)
		self.personal_id = response.json()['data'][1]['id']

	def check_tos_accepted(self):
		url = f"https://graph.facebook.com/v10.0/{self.personal_id}?fields=tos_accepted&access_token={self.token}"
		response = requests.get(url)
		print(response.json())