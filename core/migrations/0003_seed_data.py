from django.db import migrations

def seed_data(apps, schema_editor):
    Project = apps.get_model('core', 'Project')
    Skill = apps.get_model('core', 'Skill')
    Testimonial = apps.get_model('core', 'Testimonial')

    # Seed Skills
    skills_data = [
        {"name": "Python", "percent": 95},
        {"name": "Django", "percent": 92},
        {"name": "REST APIs", "percent": 90},
        {"name": "JavaScript", "percent": 85},
        {"name": "React", "percent": 80},
        {"name": "Tailwind CSS", "percent": 88},
    ]
    for skill in skills_data:
        Skill.objects.get_or_create(name=skill["name"], defaults={"percent": skill["percent"]})

    # Seed Projects
    projects_data = [
        {
            "title": "Cloud-Based Healthcare Platform",
            "category": "Django Backend",
            "image": "projects/clinical-detail.jpg",
            "description": "A robust medical clinic detailer and appointment scheduling platform. Built with Django REST framework, featuring comprehensive role-based access control, HIPAA-compliant patient record encryption, and real-time email notification integration."
        },
        {
            "title": "AI Customer Feedback System",
            "category": "AI Integration",
            "image": "projects/clinical-detail.jpg",
            "description": "An interactive sentiment analysis dashboard that processes client inquiries and feedback using the Gemini Pro model. Features automatic category tagging, dynamic graphs with D3.js/Recharts-like interfaces, and high-performance caching."
        },
        {
            "title": "TaskFlow Kanban Organizer",
            "category": "Fullstack Web",
            "image": "projects/clinical-detail.jpg",
            "description": "A high-fidelity project management app supporting drag-and-drop Kanban boards, team workspaces, custom tag filters, and robust token-based JWT authentication."
        }
    ]
    for proj in projects_data:
        Project.objects.get_or_create(
            title=proj["title"],
            defaults={
                "category": proj["category"],
                "image": proj["image"],
                "description": proj["description"]
            }
        )

    # Seed Testimonials
    testimonials_data = [
        {
            "client_name": "Sarah Connor (CTO, HealthTech Inc.)",
            "review": "Usman is an exceptionally talented developer. He helped us migrate our legacy database to a modern Django service with zero downtime. His expertise in backend optimization is outstanding!",
            "rating": 5
        },
        {
            "client_name": "Alex Mercer (Product Lead, DevStream)",
            "review": "The REST APIs designed by Usman are blazing fast, clean, and perfectly documented. His commitment to performance and code clarity was refreshing and highly valued.",
            "rating": 5
        }
    ]
    for test in testimonials_data:
        Testimonial.objects.get_or_create(
            client_name=test["client_name"],
            defaults={
                "review": test["review"],
                "rating": test["rating"]
            }
        )

def rollback_data(apps, schema_editor):
    Project = apps.get_model('core', 'Project')
    Skill = apps.get_model('core', 'Skill')
    Testimonial = apps.get_model('core', 'Testimonial')

    Project.objects.all().delete()
    Skill.objects.all().delete()
    Testimonial.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_testimonial_remove_project_github_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_data, rollback_data),
    ]
