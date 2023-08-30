from rest_framework.views import APIView
from rest_framework.decorators import api_view
from page.api.serializers import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET", "POST"])
def UserApiView(request):
    if request.method == "GET":
        users = User.objects.all()
        user_serializers = UserSerielizers(users, many=True)
        return Response(user_serializers.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        user_serializers = UserSerielizers(data=request.data)
        if user_serializers.is_valid():
            user_serializers.save()
            return Response({"message": "Creado Exitoso"}, status=status.HTTP_200_OK)
        return Response(user_serializers, status=status.HTTP_200_OK)
