from rest_framework import serializers

from members.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'profile', 'email', 'password']

    def save(self, **kwargs):
        profile = self.validated_data['username']
        password = self.validated_data['password']
        email = self.validated_data['email']
        user = User.objects.create_user(
            profile=profile,
            password=password,
            email=email
        )
        return user
