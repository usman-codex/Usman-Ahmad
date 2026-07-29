from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.html import escape
import google.generativeai as genai
from .models import Project, Skill, ContactMessage, Testimonial

# 1. AI Configuration
API_KEY = getattr(settings, 'GEMINI_API_KEY', None)
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"
GENERATION_CONFIG = genai.types.GenerationConfig(temperature=0.4)

if API_KEY:
    genai.configure(api_key=API_KEY)

def home(request):
    context = {
        'projects': Project.objects.all().order_by('-id'),
        'skills': Skill.objects.all(),
        'testimonials': Testimonial.objects.all(),
    }
    return render(request, 'index.html', context)

def projects(request):
    context = {
        'projects': Project.objects.all().order_by('-id'),
        'skills': Skill.objects.all(),
    }
    return render(request, 'projects.html', context)

# 2. HTMX: Contact Form
def contact_submit(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, phone=phone, message=message)
        return HttpResponse(f'''
            <div class="text-center py-5">
                <i class="fas fa-check-circle text-primary" style="font-size: 60px; margin-bottom: 20px; color: #1d6bff;"></i>
                <h4 class="fw-bold mt-3" style="color: white;">Thanks {name}!</h4>
                <p style="color: #8f96aa;">Your message has been sent successfully. I'll get back to you soon.</p>
            </div>
        ''')
    return redirect('home')

# 3. HTMX: Chatbot (Single definition with your custom instructions)
def chatbot(request):
    if request.method != "POST":
        return redirect("home")

    prompt = (request.POST.get("prompt") or "").strip()
    if not prompt:
        return HttpResponse("<div class='chatbot-bubble ai'>Please ask a question.</div>")

    if not API_KEY:
        return HttpResponse("<div class='chatbot-bubble ai'>API Key missing. Please check your .env file.</div>")

    # Fetch Dynamic Data
    db_projects = Project.objects.all()
    db_skills = Skill.objects.all()
    projects_ctx = "\n".join([f"🚀 {p.title}: {p.description}" for p in db_projects])
    skills_ctx = ", ".join([f"{s.name} ({s.percent}%)" for s in db_skills])

    # YOUR PERSONALITY RULES
    system_prompt = f"""
    You are Usman Ahmad's Official AI Assistant. Represent him professionally.
    
    RULES:
    1. Never say you are Gemini, ChatGPT, or an AI. Speak as Usman's assistant.
    2. Be natural, friendly, and professional.
    3. If info is missing, say: "That information hasn't been added to my knowledge base yet."
    
    IDENTITY: 
    Usman Ahmad is a Frontend & Django Developer based in Pakistan.
    
    SKILLS FROM DATABASE: {skills_ctx}
    PROJECTS FROM DATABASE: {projects_ctx}
    
    SPECIFIC GREETINGS:
    - hi/hello: Reply "Hi 👋 I'm Usman Ahmad's AI Assistant. Usman is a Web Developer and Django Developer. How can I help you today?"
    - how are you: Reply "I'm doing great, thank you! 😊 How about you?"
    - hire/freelance: Reply "Usman is available! Contact him via WhatsApp (0328 8874142) or Email (usmancodex.dev@gmail.com)."
    """

    try:
        model = genai.GenerativeModel(DEFAULT_GEMINI_MODEL)
        
        response = model.generate_content(
            f"{system_prompt}\n\nUser: {prompt}\nAssistant:",
            generation_config=GENERATION_CONFIG
        )

        if response.candidates and response.candidates[0].content.parts:
            answer = response.text
        else:
            answer = "I apologize, but I couldn't generate a response for that. It might have been flagged by safety filters. Could you try asking in a different way?"

    except Exception as e:
        # Logging the full error to the terminal for debugging
        import traceback
        print("--- FULL ERROR START ---")
        traceback.print_exc() 
        print("--- FULL ERROR END ---")

        error_msg = str(e)
        if "404" in error_msg:
            answer = "I'm having trouble connecting to my AI model. Please ensure the 'google-generativeai' package is updated on the server."
        elif "API_KEY_INVALID" in error_msg:
            answer = "It looks like the API key is invalid. Please check the .env file."
        else:
            answer = "I encountered a connection error. Please try again in a moment."

    safe_prompt = escape(prompt)
    safe_answer = escape(answer).replace("\n", "<br>")

    # Return HTML + Javascript to handle UI (scroll & clear input)
    return HttpResponse(f"""
    <div class="chatbot-message-pair animate__animated animate__fadeIn" style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; width: 100%;">
        <div style="display: flex; justify-content: flex-end; width: 100%;">
            <div class='chatbot-bubble user' style='background: #1e2125; color: white; padding: 12px 18px; border-radius: 18px 18px 0 18px; max-width: 85%;'>{safe_prompt}</div>
        </div>
        <div style="display: flex; justify-content: flex-start; width: 100%;">
            <div class='chatbot-bubble ai' style='background: #ff014f; color: white; padding: 12px 18px; border-radius: 18px 18px 18px 0; max-width: 85%;'>{safe_answer}</div>
        </div>
    </div>
    <script>
        (function() {{
            var chatContainer = document.getElementById('chatbot-messages');
            if (chatContainer) {{ chatContainer.scrollTop = chatContainer.scrollHeight; }}
            var inputField = document.querySelector('input[name="prompt"]');
            if (inputField) {{ inputField.value = ''; }}
        }})();
    </script>
    """)

# 4. HTMX: Tab Switches
def get_bio(request):
    return HttpResponse("""
    <div class='animate__animated animate__fadeIn d-grid gap-3'>
        <div class="p-3 border-start border-primary border-4" style="background: rgba(255,255,255,0.02); border-radius: 4px 12px 12px 4px; border-left: 4px solid var(--primary) !important;">
            <h5 class="fw-bold text-white mb-1" style="font-size: 1rem;"><i class="fas fa-heart text-primary me-2"></i> Coding Passion & Philosophy</h5>
            <p class="mb-0 text-muted" style="font-size: 0.9rem; color: #cdd3e6 !important;">I am deeply passionate about crafting elegant, robust backend logic and beautiful user interfaces that make web platforms fast, secure, and delightfully interactive. I love solving complex structural challenges and writing highly maintainable, clean code.</p>
        </div>
        <div class="p-3 border-start border-primary border-4" style="background: rgba(255,255,255,0.02); border-radius: 4px 12px 12px 4px; border-left: 4px solid var(--primary) !important;">
            <h5 class="fw-bold text-white mb-1" style="font-size: 1rem;"><i class="fas fa-history text-primary me-2"></i> Years of Experience</h5>
            <p class="mb-0 text-muted" style="font-size: 0.9rem; color: #cdd3e6 !important;">Over 2+ years of web development experience building backend-focused platforms, database schemas, and seamless frontend integrations.</p>
        </div>
        <div class="p-3 border-start border-primary border-4" style="background: rgba(255,255,255,0.02); border-radius: 4px 12px 12px 4px; border-left: 4px solid var(--primary) !important;">
            <h5 class="fw-bold text-white mb-1" style="font-size: 1rem;"><i class="fas fa-map-marker-alt text-primary me-2"></i> Location</h5>
            <p class="mb-0 text-muted" style="font-size: 0.9rem; color: #cdd3e6 !important;">Lahore, Pakistan (Available for Remote Worldwide Collaboration)</p>
        </div>
    </div>
    """)

def get_skills(request):
    return HttpResponse("""
    <div class='animate__animated animate__fadeIn d-grid gap-3'>
        <div class="p-3 border-start border-primary border-4" style="background: rgba(255,255,255,0.02); border-radius: 4px 12px 12px 4px; border-left: 4px solid var(--primary) !important;">
            <h5 class="fw-bold text-white mb-1" style="font-size: 1rem;"><i class="fas fa-server text-primary me-2"></i> Robust Backend Stack</h5>
            <p class="mb-0 text-muted" style="font-size: 0.9rem; color: #cdd3e6 !important;">Expertise in <strong>Python, Django, Django REST Framework (DRF), and Admin Dashboard Controlling</strong>. Skilled in designing scalable RESTful APIs, custom middle-tier routing, Django ORM, and complex queries.</p>
        </div>
        <div class="p-3 border-start border-primary border-4" style="background: rgba(255,255,255,0.02); border-radius: 4px 12px 12px 4px; border-left: 4px solid var(--primary) !important;">
            <h5 class="fw-bold text-white mb-1" style="font-size: 1rem;"><i class="fas fa-laptop-code text-primary me-2"></i> Interactive Frontend Stack</h5>
            <p class="mb-0 text-muted" style="font-size: 0.9rem; color: #cdd3e6 !important;">Advanced skills in <strong>React.js, Next.js, and ES6+ JavaScript</strong> paired with modern responsive architectures, fluid custom animations, and interactive templates for stunning user experiences.</p>
        </div>
    </div>
    """)

def get_education(request):
    return HttpResponse("""
    <div class='animate__animated animate__fadeIn d-grid gap-3'>
        <div class="p-3 border-start border-primary border-4" style="background: rgba(255,255,255,0.02); border-radius: 4px 12px 12px 4px; border-left: 4px solid var(--primary) !important;">
            <h5 class="fw-bold text-white mb-1" style="font-size: 1rem;"><i class="fas fa-network-wired text-primary me-2"></i> Professional Web Handling</h5>
            <p class="mb-0 text-muted" style="font-size: 0.9rem; color: #cdd3e6 !important;">Capable of handling core web standards: configuring CORS origins, designing JWT secure token authorizations, session cookie protection, rate limit throttling, request validation pipelines, and optimized caching.</p>
        </div>
        <div class="p-3 border-start border-primary border-4" style="background: rgba(255,255,255,0.02); border-radius: 4px 12px 12px 4px; border-left: 4px solid var(--primary) !important;">
            <h5 class="fw-bold text-white mb-1" style="font-size: 1.05rem;"><i class="fas fa-graduation-cap text-primary me-2"></i> BS in Software Engineering (BSSE)</h5>
            <p class="mb-2 text-muted" style="font-size: 0.9rem; color: #cdd3e6 !important;">Virtual University of Pakistan</p>
            <div class="d-inline-block py-1 px-3" style="background: rgba(29, 107, 255, 0.15); color: #4d94ff; font-weight: 600; font-size: 0.8rem; border-radius: 99px; width: fit-content;">2024 - 2028</div>
        </div>
    </div>
    """)