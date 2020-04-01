from rest_framework import serializers

from contents.models import Contents


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
            'actors',
            'directors',
        ]


class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = [
            'id',
            'contents_title',
            'contents_image',
        ]
