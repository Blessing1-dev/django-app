from django.contrib import admin
from .models import Issue, Module, Enrollment, InstructorProfile, ModuleSchedule, Assessment, Resource
#from .models import Registration
#from .models import Student

# Register your models here.

admin.site.register(Issue)
#Remember we've done this below @admin.register(Module), so no need for admin.site.register(Issue)
admin.site.register(Enrollment)
admin.site.register(InstructorProfile)
admin.site.register(ModuleSchedule)
admin.site.register(Assessment)
admin.site.register(Resource)
#admin.site.register(Registration)
#admin.site.register(Student)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credit', 'category', 'availability', 'short_description')
    def short_description(self, obj):
        return (obj.description[:20] + '...') if len(obj.description) > 20 else obj.description
    short_description.short_description = 'Description'
    
    fields = ('name', 'code', 'credit', 'category', 'availability', 'courses_allowed', 'description')