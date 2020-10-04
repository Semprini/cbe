from rest_framework import permissions, renderers, viewsets

from cbe.project.models import Project
from cbe.project.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer