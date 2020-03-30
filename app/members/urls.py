from django.urls import path

from members.apis import UserLogoutAPIView, CreateUserView, UserLoginAPIView, ProfileListCreateView, ProfileIconListView

urlpatterns = [
    path('', CreateUserView.as_view()),  # 회원가입
    path('login/', UserLoginAPIView.as_view()),  # 유저 로그인
    path('logout/', UserLogoutAPIView.as_view()),  # 유저 로그아웃
    path('profiles/', ProfileListCreateView.as_view()),
    path('profiles/icons/', ProfileIconListView.as_view()),
]
