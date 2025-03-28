from django.shortcuts import render
#from django.core.mail import send_mail
#from django.contrib import messages
#from .forms import ContactForm

# Create your views here.
#This code will import the object HttpResponse which will use to render the views
#from django.http import HttpResponse           #As templates now manage responses, you can remove the from django.http import HttpResponse line in views.py.

#define a function for the home view
def home(request):
    return render(request, 'itreporting/home.html', {'title': 'Welcome'})

def about(request):
    return render(request, 'itreporting/about.html', {'title': 'About'})

def contact(request):
    return render(request, 'itreporting/contact.html', {'title': 'Contact'})
    
def course(request):
    return render(request, 'itreporting/module.html', {'title': 'Module'})    
    #if request.method == 'POST':
        #form = ContactForm(request.POST)
        #if form.is_valid():
         #   name = form.cleaned_data['name']
          #  email = form.cleaned_data['email']
           # subject = form.cleaned_data['subject']
            #message = form.cleaned_data['message']

            # Send email (adjust settings as needed)
            #send_mail(
             #   f'Enquiry from {name}: {subject}',
              #  message,
               # email,
                #['admin@blessingomokarouniversity.edu'],    
                #fail_silently=False,
            #)

            #messages.success(request, "Your enquiry has been sent successfully!")
            #return render(request, 'itreporting/contact.html', {'form': ContactForm()})
    #else:
     #   form = ContactForm()
    
    #return render(request, 'itreporting/contact.html', {'form': form})

    
