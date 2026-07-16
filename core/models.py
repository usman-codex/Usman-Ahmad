from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Project(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="Web Development")
    image = models.ImageField(upload_to='projects/')
    description = models.TextField()

class Skill(models.Model):
    name = models.CharField(max_length=50)
    percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)]) # e.g., 90 for 90%

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])