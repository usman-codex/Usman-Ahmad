from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    # Using underscores to match the function names and reduce confusion
    path('contact_submit/', views.contact_submit, name='contact_submit'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('get-bio/', views.get_bio, name='get_bio'),
    path('get-skills/', views.get_skills, name='get_skills'),
    path('get-education/', views.get_education, name='get_education'),
]