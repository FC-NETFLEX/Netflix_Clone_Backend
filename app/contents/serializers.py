from rest_framework import serializers

from contents.models import Contents, Video
from members.models import Watching, Profile


class ContentsDetailSerializer(serializers.ModelSerializer):
    actors = serializers.StringRelatedField(many=True, read_only=True)
    directors = serializers.StringRelatedField(many=True, read_only=True)

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
        ]

    def to_representation(self, instance):
        profile = Profile.objects.get(pk=self.context['profile_pk'])
        is_selected = True if profile in instance.select_profiles.all() else False
        is_like = True if profile in instance.like_profiles.all() else False

        representation = super().to_representation(instance)
        representation['is_selected'] = is_selected
        representation['is_like'] = is_like
        return representation


class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = [
            'id',
            'contents_title',
            'contents_image',
        ]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'video_url'
        ]


class WatchingSerializer(serializers.ModelSerializer):
    video = VideoSerializer()

    class Meta:
        model = Watching
        fields = [
            'id',
            'video',
            'playtime'
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
