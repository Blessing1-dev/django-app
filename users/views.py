import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import logging
from datetime import datetime
from .forms import UserRegisterForm, UserUpdateForm, StudentUpdateForm
from .models import Student
from itreporting.models import Module, Registration

logger = logging.getLogger(__name__)
@login_required
def call_azure_function(request):
    if request.method == 'POST':
        payload = {
            'student': request.user.username,
            'module': request.POST.get('module', 'ECO101'),  # Default to CS101 if not provided
            'email': request.user.email,
            'action': 'registered',  # or 'unregistered' depending on context
            'date': str(datetime.now().date())  # Include the current date
        }
        
        azure_url = 'https://ardenthorizonuni.azurewebsites.net/api/http_trigger1?code=ymJzicNJp5oc_8Lr2FjPREm__-jD1b29hoG1d2vMwOuzAzFuEY-yvA=='

        try:
            response = requests.post(azure_url, json=payload)
            response.raise_for_status()
            result = response.json()
            return JsonResponse({'status': 'success', 'azure_response': result})
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Azure function: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def send_registration_email(request):
    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['email', 'module', 'action', 'date']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return JsonResponse({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)
            
            # Process the email sending logic using data
            student = data.get('student', 'Unknown Student')
            email = data['email']
            module = data['module']
            action = data['action']
            date = data['date']
            
            logger.info(f"Student: {student}, Email: {email}, Module: {module}, Action: {action}, Date: {date}")
            # You can add the code to send an email here (this is a placeholder)
            # Example: send_email_to_user(email, module, action, date)

            return JsonResponse({"message": "Email sent successfully!"}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            logger.error(f"Error processing registration email: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)
            messages.success(request, 'Account created! Now you can login!')
            return redirect('login')
        else:
            messages.warning(request, 'Unable to create account.')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Student Registration'})

logger = logging.getLogger(__name__)

@login_required
def register_module(request, code):
    student = request.user.student
    module = get_object_or_404(Module,code=code)
    
    if not Registration.objects.filter(student=student, module=module).exists():
        Registration.objects.create(student=student, module=module)
        messages.success(request, f'You have successfully registered for the {module.name} module.')

        #Call Azure Function after successful registration
        payload = {
            'student': request.user.username,
            'module': module.name,
            'email': request.user.email,
            "action": "registered",
            "date": str(datetime.now().date())
        }
        
        azure_url = 'https://ardenthorizonuni.azurewebsites.net/api/http_trigger1?code=ymJzicNJp5oc_8Lr2FjPREm__-jD1b29hoG1d2vMwOuzAzFuEY-yvA=='


        try:
            response = requests.post(azure_url, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error calling Azure Function: {str(e)}")

    else:
        messages.error(request, f'You are already registered for the {module.name} module.')

    
    return redirect('itreporting:module_list')


@login_required
def unregister_module(request, code):
    student = request.user.student
    module = get_object_or_404(Module, code=code)
    registration = Registration.objects.filter(student=student, module=module).first()

    if registration:
        registration.delete()
        messages.success(request, f'You have successfully unregistered from the {module.name} module.')

        # Azure Function payload
        payload = {
            'student': request.user.username,
            'module': module.name,
            'email': request.user.email,
            'action': 'unregistered',
            'date': str(datetime.now().date())
        }

        azure_url = 'https://ardenthorizonuni.azurewebsites.net/api/http_trigger1?code=ymJzicNJp5oc_8Lr2FjPREm__-jD1b29hoG1d2vMwOuzAzFuEY-yvA=='


        try:
            response = requests.post(azure_url, json=payload)
            response.raise_for_status()
            print(f"Azure Function response: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error calling Azure Function: {str(e)}")

    else:
        messages.error(request, f'You are not registered for the {module.name} module.')

    return redirect('itreporting:module_list')


@login_required
def student_profile(request):
    student = request.user.student
    registrations = student.registration_set.all()
    available_modules = Module.objects.exclude(id__in=[r.module.id for r in registrations])

    return render(request, 'users/student.html', {
        'student': student,
        'registrations': registrations,
        'available_modules': available_modules
    })


@login_required
def update_profile(request):
    student = request.user.student
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = StudentUpdateForm(request.POST, request.FILES, instance=student)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been successfully updated!')
            return redirect('users:student')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = StudentUpdateForm(instance=student)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Student Profile'
    }

    return render(request, 'users/student.html', context)
