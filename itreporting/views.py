from django.shortcuts import render
from .models import Issue
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.views.generic.edit import DeleteView, FormView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .forms import ContactForm
from django.contrib import messages
#from .models import Issues


# Create your views here.
#This code will import the object HttpResponse which will use to render the views
#from django.http import HttpResponse           #As templates now manage responses, you can remove the from django.http import HttpResponse line in views.py.

#define a function for the home view
def home(request):
    import requests
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    cities = [('Sheffield', 'UK'), ('Melaka', 'Malaysia'), ('Bandung', 'Indonesia')]
    weather_data = []
    api_key = '<put your API key here>'

    for city in cities:
        city_weather = requests.get(url.format(city[0], city[1], api_key)).json() # Request the API data and convert the JSON to Python data types
    
        if 'name' in city_weather and 'main' in city_weather and 'weather' in city_weather and 'sys' in city_weather:
            weather = {
                'city': city_weather['name'] + ', ' + city_weather['sys']['country'],
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
            }   
            weather_data.append(weather) # Add the data for the current city into our list
        else:
            print(f"Error fetching data for {city}: {city_weather}")
    return render(request, 'itreporting/home.html', {'title': 'Homepage', 'weather_data': weather_data})
    #return render(request, 'itreporting/home.html', {'title': 'Welcome'})

def about(request):
    return render(request, 'itreporting/about.html', {'title': 'About'})

def module(request):
    return render(request, 'itreporting/module.html', {'title': 'Module'})

def report(request):
   
    daily_report = {'issues': Issue.objects.all(), 'title': 'Issues Reported'}
    return render(request, 'itreporting/report.html', daily_report)

class PostListView(ListView):
    model = Issue
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 5  # Optional pagination

class UserPostListView(ListView): 
    model = Issue
    template_name = 'itreporting/user_issues.html' 
    context_object_name = 'issues'
    paginate_by = 5


    def get_queryset(self):

        user=get_object_or_404(User, username=self.kwargs.get('username'))

        return Issue.objects.filter(author=user).order_by('-date_submitted')
    
class PostDetailView(DetailView):
    model = Issue
    template_name = 'itreporting/issue_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    fields = ['type', 'room', 'urgent', 'details']

    def form_valid(self, form): 

        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Issue
    fields = ['type', 'room', 'details']
    
    def test_func(self):

        issue = self.get_object()

        return self.request.user == issue.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Issue
    success_url = '/report'
    
    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author
        
class ContactFormView(FormView): 

    form_class = ContactForm 
    template_name = 'itreporting/contact.html' 

    def get_context_data(self, **kwargs): 

        context = super(ContactFormView, self).get_context_data(**kwargs) 
        context.update({'title': 'Contact Us'}) 
        return context 

    def form_valid(self, form): 
        form.send_mail() 
        messages.success(self.request, 'Successfully sent the enquiry') 
        return super().form_valid(form) 

    def form_invalid(self, form): 
        messages.warning(self.request, 'Unable to send the enquiry') 
        return super().form_invalid(form)  

    def get_success_url(self): 
        return self.request.path 
    
