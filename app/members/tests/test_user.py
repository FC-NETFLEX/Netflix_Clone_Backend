import pytest
from django.urls import reverse
from rest_framework import status

from members.serializers import UserCreateSerializer


@pytest.mark.django_db
def test_user_model(django_user_model):
    """
    - User 생성 테스트
        1. 일반 유저 생성 테스트
        2. 슈퍼 유저 생성 테스트
    """

    # 1. 일반 유저 테스트
    email = "test@test.com"
    password = "test"
    user = django_user_model.objects.create_user(email=email, password=password)
    assert user.is_superuser is False
    assert user.is_staff is False
    assert user.is_active is True
    assert user.email == email
    assert user.check_password(password) is True

    # 2. superuser 테스트
    email = "admin@admin.com"
    password = "admin"
    user = django_user_model.objects.create_superuser(email=email, password=password)
    assert user.is_superuser is True
    assert user.is_staff is True
    assert user.is_active is True
    assert user.email == email
    assert user.check_password(password) is True


@pytest.mark.django_db
class TestAuthToken:
    pytestmark = pytest.mark.django_db

    def test_user_create(self, api_client, django_user_model):
        url = reverse('members:user-create-view')
        data = {
            "email": "test2@test2.com",
            "password": "1234"
        }

        response = api_client.post(url, data)

        user = django_user_model.objects.get(email=response.data.get('email'))
        serializer = UserCreateSerializer(user)

        assert user.email == serializer.data['email']

    def test_user_auth_token(self, api_client, django_user_model):
        url = reverse('members:auth-token-view')
        user = django_user_model.objects.create_user(email='test2@test2.com', password='1234')
        # user Authentication 성공
        data = {
            "email": user.email,
            "password": "1234"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        assert response.data.get('token') == user.auth_token.key

        # user Authentication 실패
        data = {
            "email": user.email,
            "password": "12345"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
