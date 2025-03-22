from django.shortcuts import render

# Create your views here.
#This code will import the object HttpResponse which will use to render the views
#from django.http import HttpResponse           #As templates now manage responses, you can remove the from django.http import HttpResponse line in views.py.

#define a function for the home view
def home(request):
    return render(request, 'itreporting/home.html')

def about(request):
    return render(request, 'itreporting/about.html')

def contact(request):
    return render(request, 'itreporting/contact.html')
