from django.urls import path

from members.apis import GetUserInfoAPIView, AuthTokenAPIView, LogoutAPIView, CreateUserAPIView

urlpatterns = [
    path('', CreateUserAPIView.as_view()),  # 회원가입
    path('login/', AuthTokenAPIView.as_view()),  # 유저 로그인
    path('logout/', LogoutAPIView.as_view()),  # 유저 로그아웃
]
