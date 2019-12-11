from rest_framework import permissions, renderers, viewsets
from rest_framework.response import Response

from cbe.trouble.models import Problem
from cbe.trouble.serializers import ProblemSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
