import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";
import { GoogleGenAI } from "@google/genai";

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;
const HOST = '0.0.0.0';

// Configure EJS View Engine
app.set("view engine", "ejs");
const viewsPath = __dirname.endsWith("dist")
  ? path.join(__dirname, "..", "views")
  : path.join(__dirname, "views");
app.set("views", viewsPath);

// Middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use("/media", express.static(path.join(process.cwd(), "media")));
app.use("/static", express.static(path.join(process.cwd(), "core", "static")));

// Helper function to escape HTML
function escapeHtml(unsafe: string): string {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// In-Memory Database / Seed Data
const projects = [
  {
    id: 1,
    title: "Django Task Manager REST API",
    category: "Backend Development",
    description: "A comprehensive task management REST API built with Django and Django REST Framework, featuring JWT authentication, task filtering, sorting, and user-specific permissions.",
    image: "/media/projects/django-api.jpg",
    fallback_image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80",
    tags: ["Django", "REST API", "JWT", "Python"]
  },
  {
    id: 2,
    title: "Enterprise Admin Dashboard Controller",
    category: "Dashboard Controlling",
    description: "A robust systems administrator dashboard featuring dynamic telemetry tracking, user group authorization tables, live active connection logs, and customizable rate limit switches.",
    image: "/media/projects/admin-dashboard.jpg",
    fallback_image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80",
    tags: ["React.js", "Dashboard", "Tailwind CSS", "Systems Control"]
  },
  {
    id: 3,
    title: "E-Commerce Backend Engine",
    category: "Backend Development",
    description: "Robust e-commerce backend with advanced catalog search indexes, secure checkout session state integration, complex order placement transactions, and automated background notifications.",
    image: "/media/projects/ecommerce-backend.jpg",
    fallback_image: "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&q=80",
    tags: ["Django ORM", "Python", "PostgreSQL", "CORS"]
  },
  {
    id: 4,
    title: "Real-Time System Analytics Socket",
    category: "System Integration",
    description: "A lightning-fast server performance and chat hub utilizing Django Channels, WebSockets, and Redis to push live telemetry updates, typing activity state, and instantly persistent threads.",
    image: "/media/projects/analytics-socket.jpg",
    fallback_image: "https://images.unsplash.com/photo-1611746872915-64382b5c76da?auto=format&fit=crop&w=800&q=80",
    tags: ["WebSockets", "Django Channels", "Redis", "Real-Time"]
  },
  {
    id: 5,
    title: "Supabase CRM & Lead Flow Manager",
    category: "Cloud Database Integration",
    description: "A high-fidelity client relationship tracker featuring live state updates, automatic database level trigger workflows, custom user profile syncs, and multi-tenant isolation.",
    image: "/media/projects/supabase-crm.jpg",
    fallback_image: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
    tags: ["Supabase", "React.js", "PostgreSQL", "Real-Time DB"]
  },
  {
    id: 6,
    title: "Firebase Centralized Authentication Suite",
    category: "System Integration",
    description: "A complete authentication and security panel featuring federated single sign-on (SSO), live firestore user document sync, role checks, and modern multi-step security validation.",
    image: "/media/projects/firebase-auth.jpg",
    fallback_image: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
    tags: ["Firebase", "Auth", "Firestore", "Secure Sessions"]
  }
];

const skills = [
  { id: 1, name: "Python", percent: 95 },
  { id: 2, name: "Django", percent: 90 },
  { id: 3, name: "REST APIs", percent: 88 },
  { id: 4, name: "React.js", percent: 75 },
  { id: 5, name: "Bootstrap & CSS", percent: 80 }
];

const testimonials = [
  {
    id: 1,
    client_name: "Fresh Salad",
    review: "The website upgrade transformed our brand online. Expert communication, fast delivery, and a beautiful final product.",
    rating: 5
  },
  {
    id: 2,
    client_name: "La Mera",
    review: "Professional service with clear results. My e-commerce store now loads faster and converts better than ever.",
    rating: 5
  }
];

// Initialize Gemini Client
const apiKey = process.env.GEMINI_API_KEY;
let aiClient: GoogleGenAI | null = null;

if (apiKey) {
  aiClient = new GoogleGenAI({
    apiKey: apiKey,
    httpOptions: {
      headers: {
        'User-Agent': 'aistudio-build',
      }
    }
  });
}

// 1. Home Route
app.get("/", (req, res) => {
  res.render("index", { projects, skills, testimonials });
});

// Route to display all projects on a separate page
app.get("/projects", (req, res) => {
  res.render("projects", { projects, skills });
});

// 2. HTMX Tab Routes
app.get("/api/bio", (req, res) => {
  res.send(`
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
  `);
});

app.get("/api/skills", (req, res) => {
  res.send(`
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
  `);
});

app.get("/api/education", (req, res) => {
  res.send(`
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
  `);
});

// 3. Contact Submission Route
app.post("/api/contact-submit", (req, res) => {
  const { name, email, phone, message } = req.body;
  console.log(`Contact message from ${name} (${email}): ${message}`);
  res.send(`
    <div class="text-center py-5">
        <i class="fas fa-check-circle text-primary" style="font-size: 60px; margin-bottom: 20px;"></i>
        <h4 class="fw-bold mt-3">Thanks ${name}!</h4>
        <p style="color: var(--muted);">Your message has been sent successfully. I'll get back to you soon.</p>
    </div>
  `);
});

// 4. Testimonial Submission Route
app.post("/api/review-submit", (req, res) => {
  const { name, message } = req.body;
  const newTestimonial = {
    id: testimonials.length + 1,
    client_name: name || "Anonymous Client",
    review: message || "Excellent development services!",
    rating: 5
  };
  testimonials.unshift(newTestimonial);

  const testimonialsHtml = testimonials.map(t => {
    const initial = (t.client_name ? t.client_name[0] : 'A').toUpperCase();
    return `
    <div class="testimonial-card animate__animated animate__fadeIn">
        <div class="d-flex align-items-center gap-3 mb-3">
            <div class="avatar-circle" style="width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, var(--primary) 0%, #4d94ff 100%); display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; font-size: 1.05rem; box-shadow: 0 4px 12px rgba(29, 107, 255, 0.25);">
                ${escapeHtml(initial)}
            </div>
            <div>
                <strong class="text-white d-block" style="margin-bottom: 0; font-size: 1.05rem;">${escapeHtml(t.client_name)}</strong>
                <span class="text-muted" style="font-size: 0.8rem;">Verified Client</span>
            </div>
        </div>
        <p style="font-style: italic; color: #cdd3e6; line-height: 1.8;">“${escapeHtml(t.review)}”</p>
    </div>
    `;
  }).join("");

  res.send(testimonialsHtml);
});

// 5. Chatbot Assistant Route
app.post("/api/chatbot", async (req, res) => {
  const prompt = (req.body.prompt || "").trim();

  if (!prompt) {
    return res.send("<div class='chatbot-bubble ai'>Please ask a question.</div>");
  }

  if (!apiKey || !aiClient) {
    return res.send("<div class='chatbot-bubble ai'>API Key missing. Please configure GEMINI_API_KEY in Settings > Secrets.</div>");
  }

  // Create Context for Gemini
  const projectsCtx = projects.map(p => `🚀 ${p.title}: ${p.description}`).join("\n");
  const skillsCtx = skills.map(s => `${s.name} (${s.percent}%)`).join(", ");

  const systemPrompt = `
You are Usman Ahmad's Official AI Assistant. Represent him professionally.

RULES:
1. Never say you are Gemini, ChatGPT, or an AI. Speak as Usman's assistant.
2. Be natural, friendly, and professional.
3. If info is missing, say: "That information hasn't been added to my knowledge base yet."

IDENTITY: 
Usman Ahmad is a Frontend & Django Developer based in Pakistan.

SKILLS FROM DATABASE: ${skillsCtx}
PROJECTS FROM DATABASE: ${projectsCtx}

SPECIFIC GREETINGS:
- hi/hello: Reply "Hi 👋 I'm Usman Ahmad's AI Assistant. Usman is a Web Developer and Django Developer. How can I help you today?"
- how are you: Reply "I'm doing great, thank you! 😊 How about you?"
- hire/freelance: Reply "Usman is available! Contact him via WhatsApp (0322 7690800) or Email (usmancodex.dev@gmail.com)."
`;

  let answer = "";
  try {
    const result = await aiClient.models.generateContent({
      model: "gemini-3.5-flash",
      contents: `${systemPrompt}\n\nUser: ${prompt}\nAssistant:`,
    });

    answer = result.text || "I apologize, but I couldn't generate a response for that. Could you try asking in a different way?";
  } catch (error: any) {
    console.error("Gemini Generation Error:", error);
    const errorMsg = error.message || "";
    if (errorMsg.includes("404")) {
      answer = "I'm having trouble connecting to the AI model. Please ensure the Google GenAI SDK is correctly configured.";
    } else if (errorMsg.includes("API_KEY_INVALID")) {
      answer = "The API key configured seems to be invalid. Please check your GEMINI_API_KEY in the Secrets settings.";
    } else {
      answer = "I encountered an issue connecting to the AI service. Please try again in a moment.";
    }
  }

  const safePrompt = escapeHtml(prompt);
  const safeAnswer = escapeHtml(answer).replace(/\n/g, "<br>");

  res.send(`
    <div class="chatbot-message-pair animate__animated animate__fadeIn" style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; width: 100%;">
        <div style="display: flex; justify-content: flex-end; width: 100%;">
            <div class='chatbot-bubble user' style='background: rgba(255,255,255,0.06); color: white; padding: 12px 18px; border-radius: 18px 18px 0 18px; max-width: 85%; border: 1px solid rgba(255,255,255,0.12);'>${safePrompt}</div>
        </div>
        <div style="display: flex; justify-content: flex-start; width: 100%;">
            <div class='chatbot-bubble ai' style='background: var(--primary); color: white; padding: 12px 18px; border-radius: 18px 18px 18px 0; max-width: 85%;'>${safeAnswer}</div>
        </div>
    </div>
    <script>
        (function() {
            var chatContainer = document.getElementById('chat-popup-body');
            if (chatContainer) { chatContainer.scrollTop = chatContainer.scrollHeight; }
            var mainChatContainer = document.getElementById('chatbot-res');
            if (mainChatContainer) {
                // For the main chatbot panel, append the messages
                var wrapper = document.createElement('div');
                wrapper.innerHTML = \`
                    <div class="chatbot-message-pair animate__animated animate__fadeIn" style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; width: 100%;">
                        <div style="display: flex; justify-content: flex-end; width: 100%;">
                            <div class='chatbot-bubble user' style='background: rgba(255,255,255,0.06); color: white; padding: 12px 18px; border-radius: 18px 18px 0 18px; max-width: 85%; border: 1px solid rgba(255,255,255,0.12);'>${safePrompt}</div>
                        </div>
                        <div style="display: flex; justify-content: flex-start; width: 100%;">
                            <div class='chatbot-bubble ai' style='background: var(--primary); color: white; padding: 12px 18px; border-radius: 18px 18px 18px 0; max-width: 85%;'>${safeAnswer}</div>
                        </div>
                    </div>
                \`;
                // If it's the placeholder, clear it first
                if (mainChatContainer.querySelector('.chatbot-placeholder')) {
                    mainChatContainer.innerHTML = '';
                }
                mainChatContainer.appendChild(wrapper);
                mainChatContainer.scrollTop = mainChatContainer.scrollHeight;
            }
            document.querySelectorAll('[name="prompt"]').forEach(function(el) { el.value = ''; });
        })();
    </script>
  `);
});

// Start Server
app.listen(PORT, HOST, () => {
  console.log(`Server running on http://${HOST}:${PORT}`);
});
