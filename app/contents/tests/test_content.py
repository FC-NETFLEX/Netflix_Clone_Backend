from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from contents.models import Contents
from members.models import User, Profile


class ContentsTest(APITestCase):
    def setUp(self):
        self.profile = baker.make_recipe(
            'contents.profile_kids'
        )

    def test_contents_list(self):
        self.user = baker.make(User, _quantity=1)
        self.profile = baker.make(Profile, _quantity=1)
        self.contents = baker.make(Contents, _quantity=2)

        self.assertEqual(len(self.user), 1)
        self.assertEqual(len(self.profile), 1)
        self.assertEqual(len(self.contents), 2)
        for profile in self.profile:
            url = reverse('content-list-view', kwargs={'profile_pk': profile.pk})

            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 6)
