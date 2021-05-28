from django.urls import path

from .views import *

urlpatterns = [
	path('demo/', Demo.as_view(), name='demo'), # Demo Testing URL
	path('campaign/', Campaign.as_view(), name='campaign'), # Create Campaign URL
	path('get_business_users/', BusinessUsers.as_view(), name='get_business_users'), # Create Campaign URL
	path('profile/', Profile.as_view(), name='profile'), # Profile URL
]