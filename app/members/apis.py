from django.contrib.auth import authenticate
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import User, Profile, ProfileIconCategory
from members.serializers import UserCreateSerializer, ProfileSerializer, \
    ProfileCreateUpdateSerializer, ProfileIconCategorySerializer


# 로그인
class AuthTokenAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
        else:
            raise AuthenticationFailed()

        data = {
            'token': token.key
        }
        return Response(data)


# 회원가
class CreateUserView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)


# profile 생성, profile list 처리
class ProfileListCreateView(generics.ListCreateAPIView):

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user).order_by('pk')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfileSerializer
        return ProfileCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileCreateUpdateSerializer

    def get_object(self):
        profile = get_object_or_404(Profile, pk=self.kwargs.get('pk'))
        return profile

    def perform_destroy(self, instance):
        instance.watching_videos.clear()
        instance.select_contents.clear()
        instance.like_contents.clear()
        super().perform_destroy(instance)


# profile icon 선택 창에 icon list를 보여줌
class ProfileIconListView(generics.ListAPIView):
    serializer_class = ProfileIconCategorySerializer
    queryset = ProfileIconCategory.objects.all()
