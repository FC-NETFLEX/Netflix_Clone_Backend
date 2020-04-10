from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from contents.models import Contents
from contents.serializers import ContentsDetailSerializer, ContentsSerializer, WatchingSerializer, \
    PreviewContentsSerializer, WatchingCUDSerializer
from contents.utils import get_top_contents, get_ad_contents, get_preview_video, \
    get_popular_contents
from members.models import Profile, Watching


class ContentsRetrieveView(APIView):
    def get(self, request, profile_pk, contents_pk):
        contents = get_object_or_404(Contents, pk=contents_pk)
        serializer_contents = ContentsDetailSerializer(contents, context={'profile_pk': profile_pk})
        similar_contents = Contents.objects.filter(categories__in=contents.categories.all())[:6]
        if similar_contents.count() < 6:
            similar_contents = similar_contents[:3]
        serializer_similar_contents = ContentsSerializer(similar_contents, many=True)

        data = {
            'contents': serializer_contents.data,
            'similar_contents': serializer_similar_contents.data
        }

        return Response(data)


class ContentsSelectListView(generics.ListAPIView):
    serializer_class = ContentsSerializer

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs.get('profile_pk'))
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


class ContentsSearchListView(generics.ListAPIView):
    serializer_class = ContentsSerializer

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs.get('profile_pk'))

        if profile.is_kids:
            queryset = Contents.objects.filter(contents_rating='전체 관람가')
        else:
            queryset = Contents.objects.all()
        keyword = self.request.query_params.get('keyword')

        contents_list = queryset.filter(
            Q(contents_title__icontains=keyword) | Q(contents_title_english__icontains=keyword))
        contents_count = contents_list.count()

        if contents_count == 0:
            contents_list = None
        elif contents_count < 21:
            extra_contents_list = get_popular_contents(queryset, count=21 - contents_count)
            contents_list = contents_list.union(extra_contents_list)
        elif contents_count > 21:
            contents_list = contents_list[:21]

        return contents_list


class ContentsListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, request, profile_pk):
        queryset = Contents.objects.all()
        profile = get_object_or_404(Profile, pk=profile_pk)
        if profile.is_kids:
            queryset = queryset.filter(contents_rating='전체 관람가')
        if request.query_params:
            category_name = request.query_params.get('category')
            queryset = queryset.filter(categories__category_name=category_name)
        return queryset

    def get(self, request, profile_pk):
        all_contents_list = self.get_queryset(request, profile_pk)

        recommend_contents_list = all_contents_list.filter(contents_pub_year__gte='2018')[:10]
        top_contents = get_top_contents(all_contents_list)
        ad_contents = get_ad_contents(all_contents_list)
        preview_contents_list = get_preview_video(all_contents_list)
        top10_contents_list = get_popular_contents(all_contents_list, count=10)
        watching_video_list = Watching.objects.filter(profile__id=profile_pk)

        serializer_all = ContentsSerializer(all_contents_list, many=True)
        serializer_recommend = ContentsSerializer(recommend_contents_list, many=True)
        serializer_top = ContentsDetailSerializer(top_contents, context={'profile_pk': profile_pk})
        serializer_ad = ContentsDetailSerializer(ad_contents, context={'profile_pk': profile_pk})
        serializer_watching_video = WatchingSerializer(watching_video_list, many=True)
        serializer_preview = PreviewContentsSerializer(preview_contents_list, many=True)
        serializer_top10 = ContentsSerializer(top10_contents_list, many=True)

        data = {
            "top_contents": serializer_top.data,
            "ad_contents": serializer_ad.data,
            "top10_contents": serializer_top10.data,
            "recommend_contents": serializer_recommend.data,
            "preview_contents": serializer_preview.data,
            "all_contents": serializer_all.data,
            "watching_video": serializer_watching_video.data
        }
        return Response(data)


class WatchingCreateView(generics.CreateAPIView):
    serializer_class = WatchingCUDSerializer
    queryset = Watching.objects.all()


class WatchingUpdateDestroyView(mixins.DestroyModelMixin,
                                generics.UpdateAPIView):
    pass
