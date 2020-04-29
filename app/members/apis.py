from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import User, Profile, ProfileIconCategory
from members.serializers import UserCreateSerializer, ProfileSerializer, \
    ProfileCreateUpdateSerializer, ProfileIconCategorySerializer


class AuthTokenAPIView(APIView):
    """
        사용자가 인증되면 token 값을 보내주는 api
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
        else:
            raise AuthenticationFailed()

        return Response({'token': token.key})


class UserCreateView(generics.CreateAPIView):
    """
    User를 생성하는 api
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)


class ProfileListCreateView(generics.ListCreateAPIView):
    """
    Profile list 를 요청하거나, Profile 생성하는 api
    """

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).order_by('pk')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfileSerializer
        return ProfileCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Profile 상세정보, 수정, 삭제 api
    """
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


class ProfileIconListView(generics.ListAPIView):
    """
    profile icon의 리스트를 보여주는 api
        - profile category 별로 보여준다.
    """
    serializer_class = ProfileIconCategorySerializer
    queryset = ProfileIconCategory.objects.all()
