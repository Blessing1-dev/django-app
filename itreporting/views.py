from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.contrib.auth.models import User

from .models import Issue, Module
from .forms import ContactForm, ModuleForm
from django.contrib import messages
from decouple import config, UndefinedValueError

# Create your views here. 
#This code will import the object HttpResponse which will use to render the views
#from django.http import HttpResponse           #As templates now manage responses, you can remove the from django.http import HttpResponse line in views.py.

#define a function for the home view
def home(request):
    import requests
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    cities = [('Sheffield', 'UK'), ('Derby', 'UK'), ('London', 'UK'), ('Valencia', 'Spain'), ('Melaka', 'Malaysia'), ('Bandung', 'Indonesia')]
    weather_data = []
    try:
        api_key = config('OPENWEATHER_API_KEY')
    except UndefinedValueError:
        api_key = None 

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

def about(request):
    return render(request, 'itreporting/about.html', {'title': 'About'})

def contact(request):
    return render(request, 'itreporting/contact.html', {'title': 'Contact'})

def module_list(request):
    modules = Module.objects.all()

    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('itreporting:module_list')
    else:
        form = ModuleForm()

    return render(request, 'modules/module_list.html', {'modules': modules, 'form': form})


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
    template_name = 'itreporting/contact.html'
    form_class = ContactForm
    success_url = '/'

    def get_context_data(self, **kwargs): 
        context = super(ContactFormView, self).get_context_data(**kwargs) 
        context.update({'title': 'Contact Us'}) 
        return context
    
    def form_valid(self, form):
        form.send_mail()
        messages.success(self.request, 'Your message was sent successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form): 
        messages.warning(self.request, 'Unable to send the enquiry') 
        return super().form_invalid(form)
    
    def get_success_url(self): 
        return self.request.path