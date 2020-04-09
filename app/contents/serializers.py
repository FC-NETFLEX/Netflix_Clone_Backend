from rest_framework import serializers

from contents.models import Contents, Video
from members.models import Watching, Profile


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'id',
            'video_url'
        ]


class ContentsDetailSerializer(serializers.ModelSerializer):
    actors = serializers.StringRelatedField(many=True, read_only=True)
    directors = serializers.StringRelatedField(many=True, read_only=True)
    videos = VideoSerializer(many=True)
    is_select = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Contents
        fields = [
            'id',
            'contents_title',
            'contents_title_english',
            'contents_summary',
            'contents_image',
            'contents_logo',
            'contents_rating',
            'contents_length',
            'contents_pub_year',
            'preview_video',
            'actors',
            'directors',
            'videos',
            'is_select',
            'is_like'
        ]

    def get_is_select(self, instance):
        profile = Profile.objects.get(pk=self.context.get('profile_pk'))
        return True if profile in instance.select_profiles.all() else False

    def get_is_like(self, instance):
        profile = Profile.objects.get(pk=self.context.get('profile_pk'))
        return True if profile in instance.like_profiles.all() else False


class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = [
            'id',
            'contents_title',
            'contents_image',
        ]


class WatchingSerializer(serializers.ModelSerializer):
    video = VideoSerializer()

    class Meta:
        model = Watching
        fields = [
            'id',
            'video',
            'profile',
            'playtime',
            'video_length'
        ]


class PreviewContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = [
            'id',
            'contents_title',
            'preview_video',
            'contents_logo'
        ]
