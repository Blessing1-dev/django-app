from django.contrib import admin
from .models import Course, Module, Enrollment, InstructorProfile, ModuleSchedule, Assessment, Resource
#from .models import Registration

# Register your models here.
#Remember we've done this below @admin.register(Module), so no need for admin.site.register(Issue)
admin.site.register(Enrollment)
admin.site.register(InstructorProfile)
admin.site.register(ModuleSchedule)
admin.site.register(Assessment)
admin.site.register(Resource)
#admin.site.register(Registration)

# Register the Course model
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description')  # optional: to show fields in the list view
    search_fields = ('name', 'code')

# Optionally register Module if not already
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credit', 'course', 'category', 'availability', 'short_description')
    def short_description(self, obj):
        return (obj.description[:20] + '...') if len(obj.description) > 20 else obj.description
    short_description.short_description = 'Description'
    
    fields = ('name', 'code', 'credit', 'course', 'category', 'availability', 'courses_allowed', 'description')