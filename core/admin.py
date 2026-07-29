from django.contrib import admin
from .models import Project, Skill, ContactMessage, Testimonial

# Register models for admin interface
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    search_fields = ('title', 'description')
    list_filter = ('category',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent')
    search_fields = ('name',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    readonly_fields = ('created_at',)
    list_filter = ('created_at',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'rating')
    search_fields = ('client_name',)
    list_filter = ('rating',)