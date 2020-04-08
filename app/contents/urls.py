from django.urls import path

from contents.apis import ContentsRetrieveListView, ContentsLikeAPIView, ContentsSelectAPIView, ContentsListView, \
    SelectContentsListAPIView

urlpatterns = [
    path('<int:profile_pk>/contents/<int:contents_pk>/', ContentsRetrieveListView.as_view()),
    path('<int:profile_pk>/contents/<int:contents_pk>/select/', ContentsSelectAPIView.as_view()),
    path('<int:profile_pk>/contents/<int:contents_pk>/like/', ContentsLikeAPIView.as_view()),
    path('<int:profile_pk>/contents/', ContentsListView.as_view()),
    path('<int:profile_pk>/contents/selects/', SelectContentsListAPIView.as_view()),
]
