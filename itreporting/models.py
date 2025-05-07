from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.urls import reverse
from users.models import Student

# Create your models here.

class Module(models.Model):
    CATEGORY_CHOICES = [ 
    ('core', 'Core'),
    ('elective', 'Elective'),
    ('general', 'General'),
    ('optional', 'Optional')
    ]
    
    AVAILABILITY_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    credit = models.PositiveIntegerField(default=3)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='General')
    availability = models.CharField(max_length=6, choices=AVAILABILITY_CHOICES, default='open')
    courses_allowed = models.ManyToManyField(Group, related_name='modules')
    description = models.TextField()

    def __str__(self):
        return f"{self.code} - {self.name}"

class Registration(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'module')  # Ensures a student can only register once per module

    def __str__(self):
        return f"{self.student.user.username} - {self.module.name}"


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'module')
        
    def __str__(self):
        return f"{self.student.username} enrolled in {self.module.name}"
        
class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    modules = models.ManyToManyField(Module, related_name='instructors')

    def __str__(self):
        return self.user.get_full_name()
    
class ModuleSchedule(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return f"{self.module.name} schedule for {self.semester}"
    
class Assessment(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True)
    date_assessed = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Assessment for {self.enrollment.student.username} in {self.enrollment.module.name}"
    
class Resource(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resources/')
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Resource: {self.title} for {self.module.name}"
    
class Issue(models.Model):
    type = models.CharField(max_length=100, choices = [('Hardware', 'Hardware'), ('Software', 'Software')])
    room = models.CharField(max_length=100)
    urgent = models.BooleanField(default = False)
    details = models.TextField()
    date_submitted = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    author = models.ForeignKey(User, related_name = 'issues', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type} Issue in {self.room}'
    
    def get_absolute_url(self):
        return reverse('itreporting:issue-detail', kwargs = {'pk': self.pk})
