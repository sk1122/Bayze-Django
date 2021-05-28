from django.db import models
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model

User = get_user_model() # Get User

class FacebookPages(models.Model):
	'''
		Used to Store Facebook Pages of User after each login
		user -> Foreign Key for User Model // Update it to SocialAccount Afterwards
		page_id -> page's id provided by Facebook
		page -> page name
		category -> List for Selected Categories of Facebook Pages
	'''

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fb_user", null=True)
	page_id = models.CharField(max_length=255, null=True, blank=True)
	page = models.CharField(max_length=255)
	category = models.JSONField(null=True)
	
	def __str__(self):
		return self.page

class AccessTokens(models.Model):
	'''
		Used to Store Facebook Access Tokens of User after each login
		user -> Foreign Key for User Model // Update it to SocialAccount Afterwards
		token -> Token
		expires_at -> expiry
	'''
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	token = models.CharField(max_length=255)
	expires_at = models.DateTimeField(
        blank=True, null=True, verbose_name=("expires at")
    )

	def __str__(self):
		return self.token

# Logic to Store FB Pages after login

import facebook, requests
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=AccessTokens) # Fired when token updates
def intercept_facebook_login(sender, instance, raw, **kwargs):
	if not raw: # If data has changed
		print(instance)
		store_pages(instance.token, instance.user)

def store_pages(token, user):
	graph = facebook.GraphAPI(access_token=token) # GraphAPI is FB's API for Querying
	page_data = graph.get_object('me/accounts') # Get data from https://graph.facebook.com/me/accounts

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

