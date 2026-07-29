from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Project(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="Web Development")
    image = models.ImageField(upload_to='projects/')
    description = models.TextField()

    @property
    def tags_list(self):
        title_lower = self.title.lower()
        cat_lower = self.category.lower()
        tags = []
        if "django" in title_lower or "django" in cat_lower:
            tags.append("Django")
        if "python" in title_lower or "python" in cat_lower:
            tags.append("Python")
        if "rest" in title_lower or "api" in title_lower or "drf" in title_lower:
            tags.append("REST API")
        if "react" in title_lower or "react" in cat_lower:
            tags.append("React.js")
        if "bootstrap" in title_lower or "css" in title_lower:
            tags.append("Bootstrap")
        if "supabase" in title_lower or "supabase" in cat_lower:
            tags.append("Supabase")
        if "firebase" in title_lower or "firebase" in cat_lower:
            tags.append("Firebase")
        if "kanban" in title_lower or "taskflow" in title_lower:
            tags.extend(["Kanban", "JWT", "Auth"])
        if "health" in title_lower or "clinic" in title_lower or "healthcare" in title_lower:
            tags.extend(["HIPAA", "API Security"])
        if "ai" in title_lower or "sentiment" in title_lower or "feedback" in title_lower:
            tags.extend(["Gemini API", "D3.js", "Caching"])
        
        # Default tags if none match
        if not tags:
            tags = ["Backend", "Web Development", "SQL"]
            
        return tags[:4]

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