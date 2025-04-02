from django.shortcuts import render
from .models import Issue
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.views.generic.edit import DeleteView

#from .models import Issues
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
    paginate_by = 10  # Optional pagination
    
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
    success_url = 'report/'
    
    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author
    
def contact(request):
    return render(request, 'itreporting/contact.html', {'title': 'Contact'})
        
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

    
