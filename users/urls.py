from django.urls import path, include
from .import views 

app_name = 'users'

urlpatterns = [
path('student/', views.student_profile, name = 'student'),
path('student/update/', views.update_profile, name='update_profile'),
]