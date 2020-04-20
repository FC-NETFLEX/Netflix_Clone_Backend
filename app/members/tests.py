from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


# Create your tests here.

class AuthAPITest(APITestCase):
    def test_token_api(self):
        url = "/members/auth_token/"
        email = "test@test.com"
        password = "test"

        user = baker.make(User, email=email)
        user.set_password(password)
        user.save()

        token = Token.objects.create(user=user)
        data = {
            "email": email,
            "password": password
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('token', response.data)

        self.assertEqual(
            response.data.get('token'),
            token.key
        )




