from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import Issue, Module, Registration
from users.models import Student
from .forms import ContactForm, ModuleForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages
from decouple import config

# Create your views here. 
#This code will import the object HttpResponse which will use to render the views
#from django.http import HttpResponse           #As templates now manage responses, you can remove the from django.http import HttpResponse line in views.py.

#define a function for the home view
def home(request):
    import requests
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    cities = [('Sheffield', 'UK'), ('Derby', 'UK'), ('London', 'UK'), ('Valencia', 'Spain'), ('Melaka', 'Malaysia'), ('Bandung', 'Indonesia')]
    weather_data = []
    api_key = config('OPENWEATHER_API_KEY')

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

@login_required
def module_list(request):
    query = request.GET.get('q')
    print(query)
    try:
        student = request.user.student
        print(student)
    except ObjectDoesNotExist:
        messages.error(request, "You need to complete your student profile first.")
        return redirect('update_profile')  # Replace with your actual profile completion page

    student = request.user.student
    registered_modules = Registration.objects.filter(student=student).values_list('module_id', flat=True)
    query = request.GET.get('q')
    category_type = request.GET.get('category_type')
    availability = request.GET.get('availability')
        
    registered_modules = Registration.objects.filter(student=student).values_list('module_id', flat=True)
    
    if request.user.is_staff:
        modules = Module.objects.all()
    else:
        modules = Module.objects.filter(courses_allowed__in=request.user.groups.all()).distinct()
    
    print("DEBUG - Filtered modules for user:", modules)
    
    if category_type:
        modules = modules.filter(category=category_type)
    
    if availability == "open":
        modules = modules.filter(availability='open')
    elif availability == "closed":
        modules = modules.filter(availability='closed')    
     
    if query:
        modules = modules.filter(
             Q(name__icontains=query) | Q(code__icontains=query))

    # Pagination
    paginator = Paginator(modules, 6)  # 6 modules per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    query_string = query_params.urlencode()

    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Module added successfully.")  # ✅ success message
            return redirect('itreporting:module_list')
    else:
    
        form = ModuleForm()
        
    context = {
        'form': form,
        'query': query,
        'category_type': category_type,
        'availability': availability,
        'page_obj': page_obj,  # Use page_obj in template
        'registered_modules': registered_modules,
    }    

    return render(request, 'modules/module_list.html', context)

@user_passes_test(lambda u: u.is_staff)
def edit_module(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('module_list')
    else:
        form = ModuleForm(instance=module)
    return render(request, 'itreporting/edit_module.html', {'form': form, 'module': module})

@user_passes_test(lambda u: u.is_staff)
def delete_module(request, pk):
    module = get_object_or_404(Module, pk=pk)
    if request.method == 'POST':
        module.delete()
        return redirect('module_list')
    return render(request, 'itreporting/confirm_delete.html', {'module': module})


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