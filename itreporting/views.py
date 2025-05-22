from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import Course, Module, Registration
from .forms import ContactForm, ModuleForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages
from decouple import config
from azure.storage.blob import BlobServiceClient
import uuid


# Create your views here. 
#This code will import the object HttpResponse which will use to render the views
#from django.http import HttpResponse           #As templates now manage responses, you can remove the from django.http import HttpResponse line in views.py.

#define a function for the home view
def restricted_view(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name='Students').exists():
        messages.warning(request, "You are not authorized to access that page.")
        return redirect('home')  
    # Otherwise, allow access
    return render(request, 'itreporting:home.html')

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
    return render(request, 'itreporting/about.html', {'title': 'About', 'weather_data': weather_data})

@login_required
def course_detail(request, code):
    course = get_object_or_404(Course, code=code)
    modules = course.modules.all()  # Related name on FK
    return render(request, 'modules/course_detail.html', {
        'course': course, 'modules': modules
    })

@login_required
def module_detail(request, code):
    module = get_object_or_404(Module, code=code)
    return render(request, 'modules/module_detail.html', {
        'module': module
    })


@login_required
def module_list(request):
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

    query = request.GET.get('q')

    try:
        student = request.user.student
    except ObjectDoesNotExist:
        messages.error(request, "You need to complete your student profile first.")
        return redirect('update_profile')  

    registered_modules = Registration.objects.filter(student=student).values_list('module_id', flat=True)
    query = request.GET.get('q')
    category_type = request.GET.get('category_type')
    availability = request.GET.get('availability')
    
    if request.user.is_staff:
        modules = Module.objects.all()
    else:
        modules = Module.objects.filter(courses_allowed__in=request.user.groups.all()).distinct()
    
     # Filter by category_type
    if category_type:
        modules = modules.filter(category=category_type)

     # Filter by availability
    if availability == "open":
        modules = modules.filter(availability='open')
    elif availability == "closed":
        modules = modules.filter(availability='closed')    
     
    if query:
        modules = modules.filter(
             Q(name__icontains=query) | Q(code__icontains=query))

    modules = modules.order_by('name')
    
    # Pagination
    paginator = Paginator(modules, 6)  # 6 modules per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

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
        'weather_data': weather_data,
    }    

    return render(request, 'modules/module_list.html', context)

@user_passes_test(lambda u: u.is_staff)
def edit_module(request, code):
    module = get_object_or_404(Module, code=code)
    
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            messages.success(request, f"Module '{module.name}' was successfully updated.")
            return redirect('itreporting:module_list')
        else:
            messages.error(request, "Failed to update the module. Please check the form.")
    else:
        form = ModuleForm(instance=module)
    return render(request, 'modules/edit_module.html', {'form': form, 'module': module})

@user_passes_test(lambda u: u.is_staff)
def delete_module(request, code):
    module = get_object_or_404(Module, code=code)
    
    if request.method == 'POST':
        module_name = module.name
        module.delete()
        messages.success(request, f"Module '{module_name}' was successfully deleted.")
        return redirect('itreporting:module_list')
    return render(request, 'modules/confirm_delete.html', {'module': module})

class ContactFormView(FormView):
    template_name = 'itreporting/contact.html'
    form_class = ContactForm
    success_url = '/'

    def get_context_data(self, **kwargs): 
        context = super(ContactFormView, self).get_context_data(**kwargs) 
        context.update({'title': 'Contact Us'}) 
        
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
        context['weather_data'] = weather_data
        return context
    
    def form_valid(self, form):
        form.send_mail()
        
            # Getting form data to save to blob
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')
        
        # Construct content
        file_content = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage:\n{message}"

        try:
            # Set up Azure Blob Storage
            connection_string = config('AZURE_BLOB_CONNECTION_STRING')
            container_name = config('AZURE_BLOB_CONTAINER_NAME')
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)

            # Generating a unique file name
            filename = f"contact_message_{uuid.uuid4()}.txt"
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

            # Upload the file
            blob_client.upload_blob(file_content, overwrite=True)

            messages.success(self.request, 'Your message was sent successfully')
        except Exception as e:
            messages.warning(self.request, f"Message sent, but error saving to storage: {e}")

        return super().form_valid(form)
    
    def form_invalid(self, form): 
        messages.warning(self.request, 'Unable to send the enquiry') 
        return super().form_invalid(form)
    
    def get_success_url(self):
        return self.success_url
