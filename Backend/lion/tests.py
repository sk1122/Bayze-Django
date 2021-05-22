from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

access_token = ''

class UserTest(APITestCase):
	def test_register_user(self):
		url = reverse('register')
		data = {
			'email': 'sk1122@gmail.com',
			'password': 'satyam@789'
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(User.objects.get().email, 'sk1122@gmail.com')

	def test_login_user(self):
		registerUrl = reverse('register')
		data = {
			'email': 'sk1122@gmail.com',
			'password': 'satyam@789'
		}
		response = self.client.post(registerUrl, data, format='json')

		loginUrl = reverse('login')
		data = {
			'email': 'sk1122@gmail.com',
			'password': 'satyam@789'
		}
		resp = self.client.post(loginUrl, data, format='json')
		
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertTrue('access_token' in resp.data['data'])
		self.assertTrue('refresh_token' in resp.data['data'])

		access_token = resp.data['data']['access_token']

		verifyTokenURL = reverse('token_verify')
		resp = self.client.post(verifyTokenURL, {'token': access_token}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)

		demoTestURL = reverse('demo')
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'abc')
		resp = self.client.get(demoTestURL, format='json')
		self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
		resp = self.client.get(demoTestURL, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)

	def test_refresh_token(self):
		registerUrl = reverse('register')
		data = {
			'email': 'sk1122@gmail.com',
			'password': 'satyam@789'
		}
		response = self.client.post(registerUrl, data, format='json')

		loginUrl = reverse('login')
		data = {
			'email': 'sk1122@gmail.com',
			'password': 'satyam@789'
		}
		resp = self.client.post(loginUrl, data, format='json')
		refresh_token = resp.data['data']['refresh_token']

		refreshTokenURL = reverse('token_refresh')
		data = {
			'refresh': refresh_token
		}
		resp = self.client.post(refreshTokenURL, data, format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('access' in resp.data)