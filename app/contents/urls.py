from django.urls import path

from contents.apis import ContentsRetrieveView, ContentsLikeAPIView, ContentsSelectAPIView, ContentsListView, \
    ContentsSelectListView, ContentsSearchListView, WatchingCreateView, WatchingUpdateDestroyView, CategoryListView

urlpatterns = [
    path('<int:profile_pk>/contents/<int:contents_pk>/', ContentsRetrieveView.as_view(), name='content-detail-view'),
    path('<int:profile_pk>/contents/<int:contents_pk>/select/', ContentsSelectAPIView.as_view(),
         name='content-select-view'),
    path('<int:profile_pk>/contents/<int:contents_pk>/like/', ContentsLikeAPIView.as_view(), name='content-like-view'),
    path('<int:profile_pk>/contents/', ContentsListView.as_view(), name='content-list-view'),
    path('<int:profile_pk>/contents/selects/', ContentsSelectListView.as_view(), name='content-select-list-view'),
    path('<int:profile_pk>/contents/search/', ContentsSearchListView.as_view(), name='content-search-view'),
    path('<int:profile_pk>/watch/', WatchingCreateView.as_view(), name='content-watching-create-view'),
    path('<int:profile_pk>/watch/<int:pk>/', WatchingUpdateDestroyView.as_view(), name='content-watching-update-view'),
    path('<int:profile_pk>/save/', CategoryListView.as_view(), name='content-category-list-view'),
]
