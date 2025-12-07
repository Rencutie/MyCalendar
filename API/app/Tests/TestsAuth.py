from rest_framework.test import APITestCase
from app.models.profile import Profile
from app.factory import ProfileFactory

class AuthTests(APITestCase):
    def test_register_creates_user_and_profile(self):
        # Arrange
        data = {'username': 'testuser', 'password': 'password', 'email': 'test@example.com'}
        # Act
        response = self.client.post('/api/auth/register/', data)
        # Assert
        self.assertEqual(response.status_code, 201) 
        self.assertTrue(Profile.objects.filter(user__username='testuser').exists())