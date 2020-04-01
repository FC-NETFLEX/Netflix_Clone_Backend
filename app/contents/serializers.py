from contents.models import Contents
from members import serializers


class ContentsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = [
            'contents_title',
            'contents_summary',
            'contents_image',
            'contents_rating',
            'contents_length',
            'contents_pub_year',
            'actors',
            'directors',
            # '프로필이 갖고있는 select_contents'
        ]
