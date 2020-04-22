from rest_framework import serializers

from contents.models import Contents, Video, Category
from members.models import Watching, Profile


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'id',
            'video_url'
        ]


class WatchingSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    contents_image = serializers.SerializerMethodField()
    contents_id = serializers.SerializerMethodField()

    class Meta:
        model = Watching
        fields = [
            'id',
            'video',
            'contents_id',
            'contents_image',
            'playtime',
            'video_length'
        ]

    def get_contents_image(self, instance):
        return instance.video.contents.contents_image.url

    def get_contents_id(self, instance):
        return instance.video.contents.id


class WatchingCUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watching
        fields = [
            'id',
            'video',
            'playtime',
            'video_length',
        ]


class ContentsDetailSerializer(serializers.ModelSerializer):
    actors = serializers.StringRelatedField(many=True, read_only=True)
    directors = serializers.StringRelatedField(many=True, read_only=True)
    categories = serializers.StringRelatedField(many=True, read_only=True)
    videos = VideoSerializer(many=True)
    is_select = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    watching = serializers.SerializerMethodField()

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
            'categories',
            'actors',
            'directors',
            'videos',
            'is_select',
            'is_like',
            'watching',
        ]

    def get_is_select(self, instance):
        profile = Profile.objects.get(pk=self.context.get('profile_pk'))
        return True if profile in instance.select_profiles.all() else False

    def get_is_like(self, instance):
        profile = Profile.objects.get(pk=self.context.get('profile_pk'))
        return True if profile in instance.like_profiles.all() else False

    def get_watching(self, instance):
        profile = Profile.objects.get(pk=self.context.get('profile_pk'))
        try:
            watching = Watching.objects.get(profile=profile, video=instance.videos.first())
            return WatchingCUDSerializer(watching).data
        except Watching.DoesNotExist:
            return None


class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = [
            'id',
            'contents_title',
            'contents_image',
        ]


class PreviewContentsSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True)

    class Meta:
        model = Contents
        fields = [
            'id',
            'contents_title',
            'preview_video',
            'contents_logo',
            'contents_image',
            'videos',
        ]


class CategoryContentsSerializer(serializers.ModelSerializer):
    contents = ContentsSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            'category_name',
            'contents',
        ]
