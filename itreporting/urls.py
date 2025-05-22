#we have to import path, else line 12 will throw a problem saying "path" is not defined
from django.urls import path
from .views import ContactFormView #PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views
from users import views as user_views

#we define the namespace of the app, so the URL can be easily recognised and traced back to the application it 
#is sourced from
app_name = "itreporting"

#we create a route or a url for the homepage and map the function to the route
urlpatterns = [ 
    path('', views.home, name='home'),    #The home view path. The empty string '' makes this the default route
    path('about/', views.about, name='about'),  #The about us page
    path('contact/', ContactFormView.as_view(), name='contact'),  #The contact us page
    path('module/', views.module_list, name='module_list'),
    path('module/<str:code>/', views.module_detail, name='module_detail'),
    path('course/<str:code>/', views.course_detail, name='course_detail'),
    path('module/<str:code>/edit/', views.edit_module, name='edit_module'),
    path('module/<str:code>/delete/', views.delete_module, name='delete_module'),
    path('register/<str:code>/', user_views.register_module, name='register_module'),
    path('unregister/<str:code>/', user_views.unregister_module, name='unregister_module'),
]

