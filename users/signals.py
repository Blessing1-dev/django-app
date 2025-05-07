from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from .models import Student

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)
        try:
            default_group = Group.objects.get(name='Computer Science')
            instance.groups.add(default_group)
            print(f"User '{instance.username}' added to group '{default_group.name}'")
        except Group.DoesNotExist:
            print(f"User groups for {instance.username}: {instance.groups.all()}")
        
@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    if hasattr(instance, 'student'):
        instance.student.save()  
    