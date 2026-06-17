# JeevanCare – Empowering India with Intelligent Care 🇮🇳

## What's New in This Version

### Frontend (Single-File, Works Without Backend)
- **JeevanCare branding** — logo, tagline, Indian tricolor strip
- **Step-by-step onboarding** — collects name, location, symptom, budget, age, conditions
- **Real-time AI analysis** — symptom NLP mapping to conditions, hospital ranking
- **Clickable hospital contact** — Phone, Email, Website, Google Maps for every hospital
- **Full insurance section** — PM-JAY, ESIC, Star Health, HDFC ERGO, National Mediclaim
  - Eligibility checker with interactive Q&A
  - Step-by-step insurance claim workflow
- **Cost breakdown with history** — yearly historical data, budget fit check
- **Treatment journey timeline** — day-by-day step walkthrough
- **Market fairness gauge** — visual meter showing value vs market rate
- **Confidence score wheel** — circular progress indicator
- **Risk personalisation** — based on age + comorbidities
- **Multilingual** — EN, Hindi, Tamil, Telugu, Bengali, Marathi
- **No funny GIFs** — removed cat/gif content completely
- **Download summary** — plain-text health summary download

### Backend (FastAPI — Optional)
- All existing endpoints preserved (`/api/query`, `/api/hospitals`, etc.)
- Enhanced insurance endpoint with full scheme details
- Fun fact endpoint updated (no GIFs)

## Running the Frontend (No Backend Needed)
Simply open `frontend/index.html` in any browser.

## Running with Backend
```bash
pip install -r requirements.txt
cd backend
uvicorn main:app --reload --port 8000
```

Then open `frontend/index.html`.

## Architecture
- **Frontend**: Pure HTML/CSS/JS — runs standalone with built-in AI engine
- **Backend**: FastAPI — optional, enhances with server-side NLP
- **Data**: In-memory hospital & procedure database (20+ hospitals, 18 procedures)

## Supported Cities
Mumbai, Delhi, Bangalore, Chennai, Hyderabad, Kolkata, Nagpur, Jaipur, Pune, Ahmedabad, Lucknow, Coimbatore, Bhopal, Visakhapatnam, Indore, Surat, Kochi, Chandigarh, Vellore, Patna, Ranchi, Guwahati

## Supported Symptoms / Conditions
Chest pain, Heart attack, Knee pain, Hip pain, Brain tumor, Appendicitis, Cataract, Kidney stone, Gallbladder, Back pain/Slip disc, Cancer, Kidney failure/Dialysis, Pregnancy/Delivery, Liver disease, Pacemaker, Diabetic foot — plus Hindi/Tamil/Telugu/Bengali keyword support.
