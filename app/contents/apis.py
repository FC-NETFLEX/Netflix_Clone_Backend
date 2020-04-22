
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from contents.models import Contents, Category
from contents.serializers import ContentsDetailSerializer, ContentsSerializer, WatchingSerializer, \
    PreviewContentsSerializer, WatchingCUDSerializer, CategoryContentsSerializer
from contents.utils import get_top_contents, get_ad_contents, get_preview_video, \
    get_popular_contents
from members.models import Profile, Watching


class ContentsRetrieveView(APIView):
    def get(self, request, profile_pk, contents_pk):
        contents = get_object_or_404(Contents, pk=contents_pk)
        serializer_contents = ContentsDetailSerializer(contents, context={'profile_pk': profile_pk})
        similar_contents = Contents.objects.filter(categories__in=contents.categories.all()).random(6)
        not_serializer_content = Contents.objects.filter(categories__in=contents.categories.all()).random(1)
        serializer_similar_contents = ContentsSerializer(similar_contents, many=True)
        while True:
            if serializer_similar_contents in serializer_contents:
                serializer_contents = not_serializer_content
            else:
                break

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
            contents_list = list(contents_list) + list(extra_contents_list)
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

        data = {
            "top_contents": ContentsDetailSerializer(top_contents, context={'profile_pk': profile_pk}).data,
            "ad_contents": ContentsDetailSerializer(ad_contents, context={'profile_pk': profile_pk}).data,
            "top10_contents": ContentsSerializer(top10_contents_list, many=True).data,
            "recommend_contents": ContentsSerializer(recommend_contents_list, many=True).data,
            "preview_contents": PreviewContentsSerializer(preview_contents_list, many=True).data,
            "watching_video": WatchingSerializer(watching_video_list, many=True).data,
        }
        return Response(data)


class WatchingCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = WatchingCUDSerializer
    queryset = Watching.objects.all()

    def perform_create(self, serializer):
        serializer.save(profile=get_object_or_404(Profile, pk=self.kwargs.get('profile_pk')))


class WatchingUpdateDestroyView(mixins.DestroyModelMixin,
                                mixins.UpdateModelMixin,
                                generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = WatchingCUDSerializer

    def get_queryset(self):
        profile_pk = self.kwargs.get('profile_pk')
        return Watching.objects.filter(profile__pk=profile_pk)

    def perform_update(self, serializer):
        serializer.save(profile=get_object_or_404(Profile, pk=self.kwargs.get('profile_pk')))

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CategoryListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoryContentsSerializer
    queryset = Category.objects.all()
