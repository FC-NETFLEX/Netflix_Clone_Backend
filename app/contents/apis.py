from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from contents.models import Contents
from contents.serializers import ContentsDetailSerializer, ContentsSerializer, WatchingSerializer, \
    PreviewContentsSerializer
from contents.utils import get_top_contents, get_ad_contents, get_preview_video, get_top10_contents
from members.models import Profile, Watching


class ContentsRetrieveListView(APIView):
    def get(self, request, profile_pk, contents_pk):
        contents = get_object_or_404(Contents, pk=contents_pk)
        serializer = ContentsDetailSerializer(contents, context={'profile_pk': profile_pk})
        return Response(serializer.data)


class SelectContentsListAPIView(generics.ListAPIView):
    serializer_class = ContentsSerializer

    def get_queryset(self):
        try:
            profile = Profile.objects.get(pk=self.kwargs.get('profile_pk'))
        except Profile.DoesNotExist:
            raise Http404
        return Contents.objects.filter(select_profiles=profile)


class ContentsLikeAPIView(APIView):
    def get(self, request, profile_pk, contents_pk):
        profile = get_object_or_404(Profile, pk=profile_pk)
        contents = get_object_or_404(Contents, pk=contents_pk)

        if profile in contents.like_profiles.all():
            contents.like_profiles.remove(profile)
        else:
            contents.like_profiles.add(profile)

        return Response(status=status.HTTP_200_OK)


class ContentsSelectAPIView(APIView):
    def get(self, request, profile_pk, contents_pk):
        profile = get_object_or_404(Profile, pk=profile_pk)
        contents = get_object_or_404(Contents, pk=contents_pk)

        if profile in contents.select_profiles.all():
            contents.select_profiles.remove(profile)
        else:
            contents.select_profiles.add(profile)

        return Response(status=status.HTTP_200_OK)


class SearchContentsListAPIView(generics.ListAPIView):
    serializer_class = ContentsSerializer

    def get_queryset(self):
        queryset = Contents.objects.all()
        keyword = self.request.query_params.get('keyword')
        return queryset.filter(Q(contents_title__icontains=keyword) | Q(contents_title_english__icontains=keyword))


class ContentsListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, profile_pk):
        all_contents = Contents.objects.all()
        profile = get_object_or_404(Profile, pk=profile_pk)
        if profile.is_kids:
            all_contents = all_contents.filter(contents_rating='전체 관람가')
        if request.query_params:
            category_name = request.query_params.get('category')
            all_contents = all_contents.filter(categories__category_name=category_name)

        recommend_contents = all_contents[:10]
        watching_video = Watching.objects.filter(profile__id=profile_pk)
        top_contents = get_top_contents(all_contents)
        ad_contents = get_ad_contents(all_contents)
        preview_contents = get_preview_video(all_contents)
        top10_contents = get_top10_contents(all_contents)

        serializer_all = ContentsSerializer(all_contents, many=True)
        serializer_recommend = ContentsSerializer(recommend_contents, many=True)
        serializer_top = ContentsDetailSerializer(top_contents, context={'profile_pk': profile_pk})
        serializer_ad = ContentsDetailSerializer(ad_contents, context={'profile_pk': profile_pk})
        serializer_watching_video = WatchingSerializer(watching_video, many=True)
        serializer_preview = PreviewContentsSerializer(preview_contents, many=True)
        serializer_top10 = ContentsSerializer(top10_contents, many=True)

        data = {
            "top_contents": serializer_top.data,
            "ad_contents": serializer_ad.data,
            "top10_contents": serializer_top10.data,
            "recommand_contents": serializer_recommend.data,
            "preview_contents": serializer_preview.data,
            "all_contents": serializer_all.data,
            "watcing_video": serializer_watching_video.data
        }
        return Response(data)
