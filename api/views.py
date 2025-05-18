#from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from itreporting.models import Registration
from itreporting.models import Issue
from itreporting.models import Module
from users.models import Student

from .serializers import IssueSerializer, ModuleSerializer, StudentSerializer, RegistrationSerializer


# Issue API ViewSet
class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all().order_by('-date_submitted')
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Registration API ViewSet
class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

# Module API ViewSet
class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Student API ViewSet
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
