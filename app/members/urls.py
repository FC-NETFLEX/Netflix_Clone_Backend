from django.urls import path

from members.apis import CreateUserView, ProfileListCreateView, \
    ProfileIconListView, AuthTokenAPIView, ProfileRetrieveUpdateDestroyView

app_name = "members"
urlpatterns = [
    path('', CreateUserView.as_view(), name='user-create-view'),  # 회원가입
    path('auth_token/', AuthTokenAPIView.as_view(), name='auth-token-view'),  # 유저 로그인
    path('profiles/', ProfileListCreateView.as_view(), name='profile-list-create-view'),
    path('profiles/<int:pk>/', ProfileRetrieveUpdateDestroyView.as_view(), name='profile-detail-update-destroy-view'),
    path('profiles/icons/', ProfileIconListView.as_view(), name='profile-icon-list-view'),
]
