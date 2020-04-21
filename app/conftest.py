import pytest


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_user(db, django_user_model):
    import uuid
    from rest_framework.authtoken.models import Token

    def make_user_and_token(**kwargs):
        if 'password' not in kwargs:
            kwargs['password'] = None
        if 'email' not in kwargs:
            kwargs['email'] = str(uuid.uuid4())
        user = django_user_model.objects.create_user(**kwargs)
        token = Token.objects.create(user=user)
        return user, token

    return make_user_and_token


@pytest.fixture
def create_icon_category_and_icon(db):
    import uuid
    import os
    from config.settings.base import ROOT_DIR
    from members.models import ProfileIconCategory, ProfileIcon
    from django.core.files.uploadedfile import SimpleUploadedFile

    def make_icon(**kwargs):
        image_path = os.path.join(ROOT_DIR, 'test_image.png')
        for i in range(2):
            ProfileIconCategory.objects.create(category_name=uuid.uuid4())
        c1, c2 = ProfileIconCategory.objects.all()
        for i in range(5):

            icon1 = ProfileIcon.objects.create(icon_category=c1, icon_name=uuid.uuid4())
            icon1.icon = SimpleUploadedFile(name='test_image.png', content=open(image_path, 'rb').read(),
                                           content_type='image/png')
            icon1.save()

            icon2 = ProfileIcon.objects.create(icon_category=c2, icon_name=uuid.uuid4())
            icon2.icon = SimpleUploadedFile(name='test_image.png', content=open(image_path, 'rb').read(),
                                            content_type='image/png')
            icon2.save()
        return ProfileIcon.objects.all()

    return make_icon
