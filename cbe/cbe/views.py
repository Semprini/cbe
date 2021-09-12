import os
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

from rest_framework import serializers, viewsets

def index(request):
    return render(request, 'index.html', {
        'build_number': f'{os.environ.get("GITHUB_RUN_NUMBER", "0")}',
    })


def heartbeat(request):
    return JsonResponse({ 'build_number': f'{os.environ.get("GITHUB_RUN_NUMBER", "0")}' })

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ContentType
        fields = ('url', 'app_label', 'model', 'name', )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer    