from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from contents.models import Contents
from contents.serializers import ContentsDetailSerializer
from members.models import Profile


class ContentsRetrieveListVew(APIView):
    def get(self, contents_pk):
        contents = Contents.objects.get(pk=contents_pk)
        contents.save()
        data = {
            'contents': contents
        }
        return Response(data)

    # put: 전체수정 / patch: 부분수정
    def patch(self, request, pk):
        contents = self.get_object(pk)
        serializer = ContentsDetailSerializer(contents, data=request.data,
                                              partial=True)  # partial:부분수정 허용
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(code=201, data=serializer.data)
        return JsonResponse(code=400, data="wrong parameters")