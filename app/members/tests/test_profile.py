import pytest
from django.urls import reverse
from rest_framework import status

from members.models import Profile


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

    def test_profile_retrieve_update_destroy(self, api_client, create_user, create_profile):
        user, token = create_user(email='test@test.com')
        profile_list = create_profile(user=user)

        assert profile_list.union(Profile.objects.all(), all=False).count() == Profile.objects.count()
        api_client.credentials(HTTP_AUTHORIZATION=f'TOKEN {token.key}')

        # profile_retrieve test
        for profile in profile_list:
            url = reverse('members:profile-detail-update-destroy-view', kwargs={'pk': profile.pk})

            response = api_client.get(url)
            assert response.status_code == status.HTTP_200_OK
            assert response.data.get('profile_name') == profile.profile_name

        # profile_update test
        for profile in profile_list:
            url = reverse('members:profile-detail-update-destroy-view', kwargs={'pk': profile.pk})

            data = {
                'profile_name': 'test'
            }
            response = api_client.patch(url, data)
            assert response.status_code == status.HTTP_200_OK
            assert response.data.get('profile_name') == 'test'

        # profile_delete test
        for profile in Profile.objects.all():
            url = reverse('members:profile-detail-update-destroy-view', kwargs={'pk': profile.pk})

            response = api_client.delete(url)
            assert response.status_code == status.HTTP_204_NO_CONTENT



