#we have to import path, else line 12 will throw a problem saying "path" is not defined
from django.urls import path #, include
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView

#we add invoke the home function from views.py
from . import views

#we define the namespace of the app, so the URL can be easily recognised and traced back to the application it 
#is sourced from
app_name = "itreporting"

#we create a route or a url for the homepage and map the function to the route
urlpatterns = [ 
    path('', views.home, name='home'),    #The home view path. The empty string '' makes this the default route
    path('about/', views.about, name='about'),  #The about us page
    path('contact/', views.contact, name='contact'),  #The contact us page
    path('module/', views.module, name='module'),
    path('report/', PostListView.as_view(), name='report'),
    path('issue/', PostListView.as_view(), name='issue-list'),
    path('issue/<int:pk>', PostDetailView.as_view(), name = 'issue-detail'),
    path('issue/new', PostCreateView.as_view(), name = 'issue-create'),
    path('issue/<int:pk>/update/', PostUpdateView.as_view(), name = 'issue-update'),
    path('issue/<int:pk>/delete/', PostDeleteView.as_view(), name = 'issue-delete'),
    path('issue/<str:username>', UserPostListView.as_view(), name = 'user-issues'),
]