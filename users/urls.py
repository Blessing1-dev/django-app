from django.urls import path
from .import views 

app_name = 'users'

urlpatterns = [
path('student/', views.student_profile, name = 'student'),
path('student/update/', views.update_profile, name='update_profile'),
path('send_to_azure/', views.call_azure_function, name='send_to_azure'),  # Change to call_azure_function
]