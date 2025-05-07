from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from .forms import UserRegisterForm, UserUpdateForm, StudentUpdateForm 
from django.shortcuts import get_object_or_404
from .models import Student
from itreporting.models import Module, Registration

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created! Now you can login!')
            return redirect('login') 
        else:
            messages.warning(request, 'Unable to create account.')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Student Registration'})

@login_required
def register_module(request, module_id):
    student = request.user.student
    module = get_object_or_404(Module, id=module_id)
    if not Registration.objects.filter(student=student, module=module).exists():
        Registration.objects.create(student=student, module=module)
        messages.success(request, f'You have successfully registered for the {module.name} module.')
    else:
        messages.error(request, f'You are already registered for the {module.name} module.')
    
    return redirect('module_list')
    
@login_required
def unregister_module(request, module_id):
    student = request.user.student
    module = get_object_or_404(Module, id=module_id)
    registration = Registration.objects.filter(student=student, module=module).first()

    if registration:
        registration.delete()
        messages.success(request, f'You have successfully unregistered from the {module.name} module.')
    else:
        messages.error(request, f'You are not registered for the {module.name} module.')
    
    return redirect('module_list')

@login_required 
def student_profile(request):    
    student = request.user.student
    registrations = student.registration_set.all()  # Fetch all registrations for the student
    available_modules = Module.objects.exclude(id__in=[r.module.id for r in registrations])  # Exclude already registered modules
    
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
            return redirect('student_profile')  # Redirect to prevent form resubmission

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = StudentUpdateForm(instance=student)

    context = {
        'u_form': u_form, 
        'p_form': p_form, 
        'title': 'Student Profile'
    }
    
    return render(request, 'users/student.html', context)
