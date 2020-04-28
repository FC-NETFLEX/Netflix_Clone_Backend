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
    """
    contents 상세 정보 api
        - url로 보내주는 contents의 상세 정보와, 비슷한 컨텐츠 6개를 선정해서 보내준다.
    """

    def get(self, request, profile_pk, contents_pk):
        contents = get_object_or_404(Contents, pk=contents_pk)
        serializer_contents = ContentsDetailSerializer(contents, context={'profile_pk': profile_pk})
        similar_contents = Contents.objects.filter(Q(categories__in=contents.categories.all()),
                                                   ~Q(contents_title=contents.contents_title)).order_by('?')[:6]
        serializer_similar_contents = ContentsSerializer(similar_contents, many=True)
        data = {
            'contents': serializer_contents.data,
            'similar_contents': serializer_similar_contents.data
        }

        return Response(data)


class ContentsSelectListView(generics.ListAPIView):
    """
        특정한 profile 의 찜 한 컨텐츠 목록을 보여주는 api
    """
    serializer_class = ContentsSerializer

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs.get('profile_pk'))
        return Contents.objects.filter(select_profiles=profile)


class ContentsLikeAPIView(APIView):
    """
        contents like 처리하는 api
        TODO : ContentsLike 와 ContentsSelect 처리하는 api 합쳐서 구현해보기
    """

    def get(self, request, profile_pk, contents_pk):
        profile = get_object_or_404(Profile, pk=profile_pk)
        contents = get_object_or_404(Contents, pk=contents_pk)

        if profile in contents.like_profiles.all():
            contents.like_profiles.remove(profile)
        else:
            contents.like_profiles.add(profile)

        return Response(status=status.HTTP_200_OK)


class ContentsSelectAPIView(APIView):
    """
            contents select 처리하는 api
    """

    def get(self, request, profile_pk, contents_pk):
        profile = get_object_or_404(Profile, pk=profile_pk)
        contents = get_object_or_404(Contents, pk=contents_pk)

        if profile in contents.select_profiles.all():
            contents.select_profiles.remove(profile)
        else:
            contents.select_profiles.add(profile)

        return Response(status=status.HTTP_200_OK)


class ContentsSearchListView(generics.ListAPIView):
    """
    contents search 를 처리하는 api
        - query로 오는 keyword 로 contents 를 검색한다.
        - 결과로 나오는 queryset은 0개나 21개로 통일
            - 검색 결과가 0개일 때 : get_queryset에서 None을 리턴, Response에서는 빈 리스트를 보내준다
            - 검색 결과가 21개 미만일 때 : 검색 결과 + popular contents(like + select 가 많은 컨텐츠) 21개를 보내준다
            - 검색 결과가 21개 이상일 때 : 21개만 잘라서 보내준다.

    TODO : query 최적화 필요
    """
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
            extra_contents_list = get_popular_contents(queryset.exclude(id__in=contents_list),
                                                       count=21 - contents_count)
            contents_list = list(contents_list) + list(extra_contents_list)
        elif contents_count > 21:
            contents_list = contents_list[:21]

        return contents_list


class ContentsListView(APIView):
    """
    home 화면 데이터를 보내주는 api
        - top_contents : 2010년 이후 개봉한 영화 중 로고가 존재하는 영화를 랜덤으로 1개 선택
        - ad_contents : preview_video 가 있는 영화 중 하나를 랜덤으로 1개 선택
        - preview_contents_list : preview_video가 있고 로고가 존재하는 영화를 랜덤으로 10개 선택
        - top10_contents_list : select + like 개수가 많은 순서대로 영화를 10개 선택
        - watching_video_list : 선택된 Profile의 watching 정보를 보여준다.
    """

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
        watching_video_list = Watching.objects.filter(profile__id=profile_pk).order_by('-pk')

        data = {
            "top_contents": ContentsDetailSerializer(top_contents, context={'profile_pk': profile_pk}).data,
            "ad_contents": ContentsDetailSerializer(ad_contents, context={'profile_pk': profile_pk}).data,
            "top10_contents": ContentsSerializer(top10_contents_list, many=True).data,
            "recommend_contents": ContentsSerializer(recommend_contents_list, many=True).data,
            "preview_contents": PreviewContentsSerializer(preview_contents_list, context={'profile_pk': profile_pk},
                                                          many=True).data,
            "watching_video": WatchingSerializer(watching_video_list, many=True).data,
        }
        return Response(data)


class WatchingCreateView(generics.CreateAPIView):
    """
        Watching 정보를 생성하는 api
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = WatchingCUDSerializer
    queryset = Watching.objects.all()

    def perform_create(self, serializer):
        serializer.save(profile=get_object_or_404(Profile, pk=self.kwargs.get('profile_pk')))


class WatchingUpdateDestroyView(mixins.DestroyModelMixin,
                                mixins.UpdateModelMixin,
                                generics.GenericAPIView):
    """
         Watching 정보를 수정하거나 삭제하는 api
    """
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
    """
        카테고리별로 영화를 보여주는 api
    """
    serializer_class = CategoryContentsSerializer
    queryset = Category.objects.all()
