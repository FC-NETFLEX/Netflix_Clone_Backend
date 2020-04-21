import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProfileAPI:
    pytestmark = pytest.mark.django_db

    def test_profile_list_create(self, api_client, create_user, create_icon_category_and_icon):
        url = reverse('members:profile-list-create-view')
        user, token = create_user(email='test@test.com')
        icon_list = create_icon_category_and_icon()
        data = {
            "profile_name": "example",
            "profile_icon": icon_list[0].pk,

        }

        api_client.credentials(HTTP_AUTHORIZATION=f'TOKEN {token.key}')
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
