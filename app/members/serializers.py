from rest_framework import serializers
from rest_framework.authtoken.models import Token

from members.models import User, Profile


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def to_representation(self, instance):
        token = Token.objects.get(user=instance)
        return {
            "id": instance.id,
            "email": instance.email,
            "token": token.key
        }


class UserDetailSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all())
    token = serializers.PrimaryKeyRelatedField(source='auth_token', queryset=Token.objects.all())

    class Meta:
        model = User
        fields = ['id', 'email', 'token', 'profile']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'image', 'is_kids', 'watching_videos', 'select_contents']


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'image', 'is_kids']


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'image', 'is_kids']

