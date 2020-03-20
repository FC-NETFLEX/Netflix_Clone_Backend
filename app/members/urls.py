from django.urls import path

from members.apis import GetUserInfoAPIView, AuthTokenAPIView, LogoutAPIView, CreateUserAPIView

urlpatterns = [
    path('get-user/', GetUserInfoAPIView.as_view()),  # 유저의 정보 확인
    path('auth-token/', LogoutAPIView.as_view()),  # 유저 로그인
    path('create-user/', CreateUserAPIView.as_view()),  # 회원가입
    path('logout-user/', LogoutAPIView.as_view()),  # 유저 로그아웃
]
