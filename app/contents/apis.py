from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from contents.models import Contents
from contents.serializers import ContentsDetailSerializer
from members.models import Profile


class ContentsRetrieveListView(APIView):
    def get(self, request, profile_pk, contents_pk):
        contents = Contents.objects.get(pk=contents_pk)
        serializer = ContentsDetailSerializer(contents)
        profile = Profile.objects.get(pk=profile_pk)
        is_selected = True if profile in contents.select_profiles.all() else False
        is_like = True if profile in contents.like_profiles.all() else False
        data = {
            'contents': serializer.data,
            'is_selected': is_selected,
            'is_like': is_like,
        }
        return Response(data)


class ContentsLikeAPIView(APIView):
    def get(self, request, profile_pk, contents_pk):
        profile = Profile.objects.get(pk=profile_pk)
        contents = Contents.objects.get(pk=contents_pk)

        if profile in contents.like_profiles.all():
            contents.like_profiles.remove(profile)
        else:
            contents.like_profiles.add(profile)

        return Response(status=status.HTTP_200_OK)


class ContentsSelectAPIView(APIView):
    def get(self, request, profile_pk, contents_pk):
        profile = Profile.objects.get(pk=profile_pk)
        contents = Contents.objects.get(pk=contents_pk)

        if profile in contents.select_profiles.all():
            contents.select_profiles.remove(profile)
        else:
            contents.select_profiles.add(profile)

        return Response(status=status.HTTP_200_OK)
