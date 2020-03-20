from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from members.models import User


# 사용자로그인 > 아이디,비밀번호,이메일 전달 > 유효성검사후토큰반환
# 로그인
from members.serializers import UserCreateSerializer


class AuthTokenAPIView(APIView):
    def POST(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
        else:
            raise AuthenticationFailed()

        serializer = UserCreateSerializer(user)
        data = {
            'token': token.key,
            'user': serializer.data
        }
        return Response(data)


# 로그아웃하면 서버에서 삭제
# 로그아웃
class LogoutAPIView(APIView):
    authentication_classes = (TokenAuthentication,)  # 간단한 토큰 기반 HTTP 인증 체계를 사용함
    permission_classes = (IsAuthenticated,)  # 인증 된 사용자에 대한 액세스를 허용하고 인증되지 않은 사용자에 대한 액세스를 거부하

    def GET(self, request):
        request.user.auth_token.delete()
        return Response(data={"detail": "로그아웃 하셨습니다."}, status=status.HTTP_200_OK)


# 회원가입
class CreateUserAPIView(APIView):
    def POST(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'user': serializer.data,
                'detail': f'{request.data["email"]}로 새로운 계정을 생성하셨습니다. '
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 유저정보가져오기
class GetUserInfoAPIView(APIView):
    def GET(self, request):
        user = Token.objects.get(key=request.auth).user
        data = {
            "user": {
                "id": user.id,
                "email": user.email,
            }
        }
        return Response(data=data, status=status.HTTP_200_OK)