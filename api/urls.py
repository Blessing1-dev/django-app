from django.urls import path, include 
from rest_framework.routers import DefaultRouter 
from .views import IssueViewSet 

app_name = 'api' 
router = DefaultRouter() 
router.register('issues', IssueViewSet) 

urlpatterns = [ 
    path('', include(router.urls)), 
] 
