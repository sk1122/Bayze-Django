from django.urls import path

from .views import *

urlpatterns = [
	path('demo/', Demo.as_view(), name='demo'), # Demo Testing URL
	path('profile/', Profile.as_view(), name='profile'), # Profile URL
]