from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from members.serializers import UserCreateSerializer

User = get_user_model()


# Create your tests here.
class UserTest(TestCase):
    def test_user_model(self):
        """
        - User 생성 테스트
            1. 일반 유저 생성 테스트
            2. 슈퍼 유저 생성 테스트
        """
        # 1. 일반 유저 테스트
        email = "test@test.com"
        password = "test"
        user = User.objects.create_user(email=email, password=password)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password(password), True)

        # 2. superuser 테스트
        email = "admin@admin.com"
        password = "admin"
        user = User.objects.create_superuser(email=email, password=password)
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password(password), True)


class UserAuthTokenTest(APITestCase):
    def test_user_create(self):
        url = "/members/"
        data = {
            "email": "test2@test2.com",
            "password": "1234"
        }

        response = self.client.post(url, data)

        user = User.objects.get(email=response.data.get('email'))
        serializer = UserCreateSerializer(user)

        self.assertEqual(user.email, serializer.data['email'])

    def test_user_auth_token(self):
        url = "/members/auth_token/"
        user = User.objects.create_user(email='test2@test2.com', password='1234')
        # user Authentication 성공
        data = {
            "email": user.email,
            "password": "1234"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(
            response.data.get('token'),
            user.auth_token.key
        )

        # user Authentication 실패
        data = {
            "email": user.email,
            "password": "12345"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)