from rest_framework import serializers
from rest_framework.authtoken.models import Token

from members.models import User, Profile, ProfileIcon


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    profiles = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all())

    class Meta:
        model = User
        fields = ['id', 'email', 'profiles']


class ProfileIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileIcon
        fields = ['id',
                  'icon_name',
                  'icon',
                  'icon_category']


class ProfileSerializer(serializers.ModelSerializer):
    profile_icon = ProfileIconSerializer()

    class Meta:
        model = Profile
        fields = ['id',
                  'profile_name',
                  'profile_icon',
                  'is_kids',
                  ]


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_name',
                  'profile_icon',
                  'is_kids']

