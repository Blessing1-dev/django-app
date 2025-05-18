from rest_framework import serializers
from rest_framework.serializers import ModelSerializer , ReadOnlyField 
from itreporting.models import Issue 
from itreporting.models import Module
from users.models import Student
from itreporting.models import Registration

class IssueSerializer(ModelSerializer): 

    author = ReadOnlyField(source = 'author.username') 
    class Meta: 

            model = Issue 

            fields = ['type', 'room', 'urgent', 'details', 'date_submitted', 'author'] 

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'