from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import *

urlpatterns = [
	path('register/', RegistrationView.as_view(), name="register"),
	path('login/', LoginView.as_view(), name="login"),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]