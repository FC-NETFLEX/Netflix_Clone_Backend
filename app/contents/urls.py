from django.urls import path

from contents.apis import ContentsRetrieveView, ContentsLikeAPIView, ContentsSelectAPIView, ContentsListView, \
    ContentsSelectListView, ContentsSearchListView, WatchingCreateView, WatchingUpdateDestroyView, CategoryListView

urlpatterns = [
    path('<int:profile_pk>/contents/<int:contents_pk>/', ContentsRetrieveView.as_view()),
    path('<int:profile_pk>/contents/<int:contents_pk>/select/', ContentsSelectAPIView.as_view()),
    path('<int:profile_pk>/contents/<int:contents_pk>/like/', ContentsLikeAPIView.as_view()),
    path('<int:profile_pk>/contents/', ContentsListView.as_view()),
    path('<int:profile_pk>/contents/selects/', ContentsSelectListView.as_view()),
    path('<int:profile_pk>/contents/search/', ContentsSearchListView.as_view()),
    path('<int:profile_pk>/watch/', WatchingCreateView.as_view()),
    path('<int:profile_pk>/watch/<int:pk>/', WatchingUpdateDestroyView.as_view()),
    path('<int:profile_pk>/save/', CategoryListView.as_view()),
]
