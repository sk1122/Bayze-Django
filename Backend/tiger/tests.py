from allauth.account import app_settings as account_settings
from allauth.account.models import EmailAddress
from allauth.account.utils import user_email
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialLogin
from allauth.utils import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.urls import reverse


# class SocialAccountTests(TestCase):

#     @override_settings(
#         SOCIALACCOUNT_AUTO_SIGNUP=True,
#         ACCOUNT_SIGNUP_FORM_CLASS=None,
#         ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.NONE  # noqa
#     )
#     def test_email_address_created(self):
#         factory = RequestFactory()
#         request = factory.get('/oauth/login/callback/')
#         request.user = AnonymousUser()
#         SessionMiddleware().process_request(request)
#         MessageMiddleware().process_request(request)

#         User = get_user_model()
#         user = User.objects.create(email="sk1122@gmail.com", password="sk1122", name="satyam")

#         print('-2')
#         account = SocialAccount(user=user, provider='openid', uid='123')
#         print('-1')
#         sociallogin = SocialLogin(user=user, account=account)
#         print(sociallogin.account)
#         print('0')
#         complete_social_login(request, sociallogin)

#         print('1')
#         user = User.objects.get(
#             **{account_settings.USER_MODEL_USERNAME_FIELD: 'sk1122@gmail.com'}
#         )
#         print('2')
#         data = SocialAccount.objects.filter(user=user, uid=account.uid)
#         print(data)
#         self.assertTrue(
#             SocialAccount.objects.filter(user=user, uid=account.uid).exists()
#         )
#         print('3')
#         self.assertTrue(
#             EmailAddress.objects.filter(user=user,
#                                         email=user_email(user)).exists()
#         )
#         print('4')


class TestLoginView(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = "test@test.com"
        self.password = "password"
        self.user = get_user_model().objects.create_user(email=self.username, password=self.password)
        # EmailAddress.objects.create(user=user, email=self.username, primary=True, verified=True)

    def test_login(self):
        response = self.client.post(reverse(
            'login'), {"email": self.username, "password": self.password}
        )
        self.assertTrue(response.status_code, 200)

    def test_wrong_login(self):
        response = self.client.post(reverse(
            'login'), {"email": "bad@login.com", "password": "wrong"}
        )
        validation_error = 'The e-mail address and/or password you specified are not correct'
        self.assertTrue(response.status_code, 400)

    def test_redirect_when_authenticated(self):
        self.client.force_login(self.user)
        resp = self.client.get('http://localhost:8000/oauth/login')
        url = "http://localhost:8000/accounts/profile"
        self.assertTrue(resp.status_code, 301)