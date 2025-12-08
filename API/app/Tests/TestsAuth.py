from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from app.models.profile import Profile

User = get_user_model()

class TestsAuth(APITestCase):
    
    def setUp(self):
        # Create a standard user for testing login and refresh
        self.username = "testuser"
        self.password = "strongpassword123"
        self.email = "test@example.com"
        
        self.user = User.objects.create_user(
            username=self.username, 
            password=self.password, 
            email=self.email
        )
        
        # Define the API endpoint base paths based on your urls.py (assuming root is /api/)
        self.token_url = '/api/token/' 
        self.refresh_url = '/api/token/refresh/'
        self.register_url = '/api/auth/register/'

    
    def test_register_creates_user_and_profile(self):
        # Arrange
        data = {
            'username': self.username,
            'password': self.password,
            'email': self.email
        }

        # Act
        response = self.client.post(self.register_url, data)
        # Assert
        self.assertEqual(response.status_code, 201) 
        self.assertTrue(User.objects.filter(user__username='testuser').exists())
    
    
    def test_successful_login_returns_tokens(self):

        # Arrange
        login_data = {
            'username': self.username,
            'password': self.password
        }
        
       # Act
        response = self.client.post(self.token_url, login_data, format='json')
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertTrue(len(response.data['access']) > 0)
        self.assertTrue(len(response.data['refresh']) > 0)

    def test_login_with_incorrect_password_fails(self):
        # arrange
        login_data = {
            'username': self.username,
            'password': 'wrongpassword'
        }

        # act
        response = self.client.post(self.token_url, login_data, format='json')
        # assert

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('No active account found', response.data['detail'])

    def test_token_refresh_obtains_new_access_token(self):
        
        # 1. Get the initial tokens (Access and Refresh)
        login_data = {
            'username': self.username,
            'password': self.password
        }
        token_response = self.client.post(self.token_url, login_data, format='json')
        refresh_token = token_response.data['refresh']
        old_access_token = token_response.data['access']
        
        # 2. Use the refresh token to get a new access token
        refresh_data = {
            'refresh': refresh_token
        }
        refresh_response = self.client.post(self.refresh_url, refresh_data, format='json')
        
        # Assertions
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)
        
        # The new access token should be different from the old one
        self.assertNotEqual(refresh_response.data['access'], old_access_token)

    def test_token_refresh_with_invalid_token_fails(self):

        refresh_data = {
            'refresh': 'definitelynotarealtoken123'
        }
        
        response = self.client.post(self.refresh_url, refresh_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)