from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from itreporting.models import Issue 
from .serializers import IssueSerializer 
from rest_framework.permissions import IsAuthenticatedOrReadOnly 

# Create your views here.

class IssueViewSet(ModelViewSet): 

    queryset = Issue.objects.all().order_by('date_submitted') 

    serializer_class = IssueSerializer

    permission_classes = [IsAuthenticatedOrReadOnly] 


    def perform_create(self, serializer): 

        serializer.save(author = self.request.user) 

