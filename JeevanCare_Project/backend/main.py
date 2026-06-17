"""
JeevanCare – Empowering India with Intelligent Care
FastAPI Backend v2.0
Real-time healthcare decision engine with multilingual support
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json, math, random, re, os
from datetime import datetime

app = FastAPI(
    title="JeevanCare API",
    description="AI-powered Healthcare Decision Engine — Empowering India with Intelligent Care",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
if os.path.exists("../frontend"):
    app.mount("/app", StaticFiles(directory="../frontend", html=True), name="frontend")

# ─────────────────────────────────────────────
# HOSPITALS DATABASE (20 hospitals)
# ─────────────────────────────────────────────
HOSPITALS_DB = [
    {"id":1,"name":"Kokilaben Dhirubhai Ambani Hospital","city":"Mumbai","state":"Maharashtra","rating":4.6,"reviews":2840,"accreditation":"NABH, JCI","type":"private","beds":750,"established":2009,"emergency":True,"specializations":["Cardiology","Oncology","Neurology","Orthopedics"],"cost_index":"high","phone":"022-30999999","email":"info@kokilabenhospital.com","website":"https://www.kokilabenhospital.com","address":"Rao Saheb Achutrao Patwardhan Marg, Four Bungalows, Andheri West, Mumbai 400053"},
    {"id":2,"name":"Lilavati Hospital","city":"Mumbai","state":"Maharashtra","rating":4.4,"reviews":1920,"accreditation":"NABH","type":"private","beds":323,"established":1978,"emergency":True,"specializations":["Cardiology","Oncology","Orthopedics","Gynecology"],"cost_index":"high","phone":"022-26751000","email":"info@lilavatihospital.com","website":"https://www.lilavatihospital.com","address":"A-791, Bandra Reclamation, Bandra West, Mumbai 400050"},
    {"id":3,"name":"KEM Hospital","city":"Mumbai","state":"Maharashtra","rating":4.0,"reviews":980,"accreditation":"NABH","type":"government","beds":1800,"established":1926,"emergency":True,"specializations":["General Medicine","Surgery","Pediatrics"],"cost_index":"low","phone":"022-24136051","email":"kemhospital@gmail.com","website":"https://www.kemhospital.com","address":"Acharya Donde Marg, Parel, Mumbai 400012"},
    {"id":4,"name":"AIIMS Delhi","city":"Delhi","state":"Delhi","rating":4.7,"reviews":5200,"accreditation":"NABH","type":"government","beds":2478,"established":1956,"emergency":True,"specializations":["All Specialties"],"cost_index":"low","phone":"011-26588500","email":"director@aiims.edu","website":"https://www.aiims.edu","address":"Sri Aurobindo Marg, Ansari Nagar, New Delhi 110029"},
    {"id":5,"name":"Fortis Escorts Heart Institute","city":"Delhi","state":"Delhi","rating":4.5,"reviews":2100,"accreditation":"NABH, JCI","type":"private","beds":310,"established":1988,"emergency":True,"specializations":["Cardiology","Cardiac Surgery"],"cost_index":"high","phone":"011-47135000","email":"info@fortishealthcare.com","website":"https://www.fortishealthcare.com","address":"Okhla Road, New Delhi 110025"},
    {"id":6,"name":"Max Super Specialty Hospital","city":"Delhi","state":"Delhi","rating":4.4,"reviews":1870,"accreditation":"NABH, JCI","type":"private","beds":500,"established":2000,"emergency":True,"specializations":["Cardiology","Oncology","Neurology","Orthopedics"],"cost_index":"high","phone":"011-26515050","email":"info@maxhealthcare.in","website":"https://www.maxhealthcare.in","address":"Press Enclave Road, Saket, New Delhi 110017"},
    {"id":7,"name":"Apollo Hospitals Chennai","city":"Chennai","state":"Tamil Nadu","rating":4.6,"reviews":3100,"accreditation":"NABH, JCI","type":"private","beds":560,"established":1983,"emergency":True,"specializations":["Cardiology","Oncology","Orthopedics","Transplant"],"cost_index":"high","phone":"044-28290200","email":"enquiry@apollohospitals.com","website":"https://www.apollohospitals.com","address":"21 Greams Lane, Off Greams Road, Chennai 600006"},
    {"id":8,"name":"Government General Hospital Chennai","city":"Chennai","state":"Tamil Nadu","rating":3.9,"reviews":760,"accreditation":"NABH","type":"government","beds":2500,"established":1664,"emergency":True,"specializations":["General Medicine","Surgery","Pediatrics"],"cost_index":"low","phone":"044-25305000","email":"mgmgh@tn.gov.in","website":"https://www.mgh.tn.gov.in","address":"Park Town, Chennai 600003"},
    {"id":9,"name":"Narayana Health City","city":"Bangalore","state":"Karnataka","rating":4.4,"reviews":1800,"accreditation":"NABH, JCI","type":"private","beds":3000,"established":2000,"emergency":True,"specializations":["Cardiac Surgery","Oncology","Orthopedics","Neurology"],"cost_index":"mid","phone":"080-71222222","email":"contactus@narayanahealth.org","website":"https://www.narayanahealth.org","address":"258/A Bommasandra Industrial Area, Bangalore 560099"},
    {"id":10,"name":"Manipal Hospital Bangalore","city":"Bangalore","state":"Karnataka","rating":4.5,"reviews":2200,"accreditation":"NABH, JCI","type":"private","beds":600,"established":1991,"emergency":True,"specializations":["Cardiology","Oncology","Orthopedics","Neurology"],"cost_index":"high","phone":"080-25024444","email":"info@manipalhospitals.com","website":"https://www.manipalhospitals.com","address":"98 HAL Airport Road, Bangalore 560017"},
    {"id":11,"name":"KIMS Hospital Hyderabad","city":"Hyderabad","state":"Telangana","rating":4.4,"reviews":1650,"accreditation":"NABH","type":"private","beds":450,"established":2005,"emergency":True,"specializations":["Cardiology","Oncology","Neurology","Orthopedics"],"cost_index":"mid","phone":"040-44885000","email":"contact@kimshospitals.com","website":"https://www.kimshospitals.com","address":"1-8-31/1 Minister Road, Secunderabad 500003"},
    {"id":12,"name":"Yashoda Hospital Hyderabad","city":"Hyderabad","state":"Telangana","rating":4.3,"reviews":1420,"accreditation":"NABH","type":"private","beds":350,"established":1989,"emergency":True,"specializations":["Cardiology","Gastroenterology","Orthopedics"],"cost_index":"mid","phone":"040-45671000","email":"info@yashodahospitals.com","website":"https://www.yashodahospitals.com","address":"Behind Hari Hara Kala Bhavan, S.P. Road, Secunderabad 500003"},
    {"id":13,"name":"Wockhardt Hospital Nagpur","city":"Nagpur","state":"Maharashtra","rating":4.2,"reviews":620,"accreditation":"NABH","type":"private","beds":150,"established":2008,"emergency":True,"specializations":["Cardiology","Orthopedics","Neurology"],"cost_index":"mid","phone":"0712-6634400","email":"nagpur@wockhardthospitals.net","website":"https://www.wockhardthospitals.com","address":"1440 Trimurti Nagar, Nagpur 440022"},
    {"id":14,"name":"Orange City Hospital Nagpur","city":"Nagpur","state":"Maharashtra","rating":4.1,"reviews":540,"accreditation":"NABH","type":"private","beds":200,"established":2001,"emergency":True,"specializations":["Cardiology","General Surgery","Orthopedics"],"cost_index":"low","phone":"0712-2228888","email":"info@orangecityhospital.com","website":"https://www.orangecityhospital.com","address":"872 Central Bazar Road, Ramdaspeth, Nagpur 440010"},
    {"id":15,"name":"Government Medical College Nagpur","city":"Nagpur","state":"Maharashtra","rating":3.8,"reviews":380,"accreditation":"NABH","type":"government","beds":1200,"established":1947,"emergency":True,"specializations":["General Medicine","Surgery","Pediatrics"],"cost_index":"low","phone":"0712-2740003","email":"gmcnagpur@maharashtra.gov.in","website":"https://gmcnagpur.org","address":"Medical Square, Nagpur 440003"},
    {"id":16,"name":"AMRI Hospital Kolkata","city":"Kolkata","state":"West Bengal","rating":4.4,"reviews":1380,"accreditation":"NABH","type":"private","beds":400,"established":2003,"emergency":True,"specializations":["Cardiology","Oncology","Orthopedics"],"cost_index":"mid","phone":"033-66000000","email":"info@amrihospitals.in","website":"https://www.amrihospitals.in","address":"JC-16 & 17, Salt Lake, Kolkata 700098"},
    {"id":17,"name":"Fortis Hospital Jaipur","city":"Jaipur","state":"Rajasthan","rating":4.3,"reviews":780,"accreditation":"NABH","type":"private","beds":250,"established":2006,"emergency":True,"specializations":["Cardiology","Orthopedics","Oncology"],"cost_index":"mid","phone":"0141-2547000","email":"fortis.jaipur@fortishealthcare.com","website":"https://www.fortishealthcare.com","address":"Jawaharlal Nehru Marg, Malviya Nagar, Jaipur 302017"},
    {"id":18,"name":"SMS Hospital Jaipur","city":"Jaipur","state":"Rajasthan","rating":3.9,"reviews":560,"accreditation":"NABH","type":"government","beds":3000,"established":1934,"emergency":True,"specializations":["General Medicine","Surgery","Pediatrics"],"cost_index":"low","phone":"0141-2518888","email":"smshospitaljaipur@gmail.com","website":"https://smshospital.rajasthan.gov.in","address":"JLN Marg, Jaipur 302004"},
    {"id":19,"name":"Christian Medical College","city":"Vellore","state":"Tamil Nadu","rating":4.7,"reviews":4200,"accreditation":"NABH, JCI","type":"private","beds":2700,"established":1900,"emergency":True,"specializations":["All Specialties"],"cost_index":"mid","phone":"0416-2281000","email":"info@cmcvellore.ac.in","website":"https://www.cmcvellore.ac.in","address":"Ida Scudder Road, Vellore 632004"},
    {"id":20,"name":"Tata Memorial Hospital","city":"Mumbai","state":"Maharashtra","rating":4.5,"reviews":3800,"accreditation":"NABH","type":"government","beds":629,"established":1941,"emergency":True,"specializations":["Oncology","Cancer Surgery","Radiation"],"cost_index":"low","phone":"022-24177000","email":"info@tmc.gov.in","website":"https://tmc.gov.in","address":"Dr Ernest Borges Marg, Parel, Mumbai 400012"},
]

PROCEDURES_DB = [
    {"id":1,"name":"Coronary Angioplasty (PTCA)","spec":"Cardiology","min":120000,"max":280000,"days":4,"keywords":["angioplasty","heart blockage","stent","chest pain","heart attack","cardiac","coronary","angio","angina"],"desc":"Opens narrowed coronary arteries using a balloon catheter and stent"},
    {"id":2,"name":"Coronary Bypass (CABG)","spec":"Cardiac Surgery","min":280000,"max":600000,"days":10,"keywords":["bypass","open heart","cabg","coronary bypass","heart surgery"],"desc":"Reroutes blood flow around blocked coronary arteries"},
    {"id":3,"name":"Knee Replacement (TKR)","spec":"Orthopedics","min":180000,"max":380000,"days":7,"keywords":["knee replacement","knee pain","arthritis knee","tkr","joint pain knee","ghutna","घुटना"],"desc":"Replaces damaged knee joint with artificial implant"},
    {"id":4,"name":"Hip Replacement (THR)","spec":"Orthopedics","min":200000,"max":420000,"days":7,"keywords":["hip replacement","hip pain","hip fracture","hip surgery","kulha"],"desc":"Total replacement of hip joint"},
    {"id":5,"name":"Brain Tumor Surgery","spec":"Neurosurgery","min":350000,"max":800000,"days":14,"keywords":["brain tumor","brain cancer","brain surgery","craniotomy","head tumor"],"desc":"Surgical removal of brain tumor"},
    {"id":6,"name":"Appendectomy","spec":"General Surgery","min":40000,"max":120000,"days":3,"keywords":["appendix","appendicitis","stomach pain right","appendix pain"],"desc":"Removal of inflamed appendix"},
    {"id":7,"name":"Cataract Surgery","spec":"Ophthalmology","min":20000,"max":80000,"days":1,"keywords":["cataract","eye surgery","blurry vision","motiyabind","motiabind"],"desc":"Phacoemulsification with IOL implant"},
    {"id":8,"name":"Kidney Stone Removal (PCNL)","spec":"Urology","min":60000,"max":200000,"days":4,"keywords":["kidney stone","urinary stone","pathri","patthar","stone kidney"],"desc":"Percutaneous nephrolithotomy for kidney stones"},
    {"id":9,"name":"Gallbladder Removal","spec":"General Surgery","min":50000,"max":150000,"days":3,"keywords":["gallbladder","gallstone","pitta","stomach pain eating"],"desc":"Laparoscopic cholecystectomy"},
    {"id":10,"name":"Spine Surgery (TLIF)","spec":"Spine Surgery","min":250000,"max":600000,"days":8,"keywords":["spine surgery","back surgery","disc","slip disc","sciatica","back pain severe"],"desc":"Lumbar interbody fusion for disc disease"},
    {"id":11,"name":"Cancer Chemotherapy (per cycle)","spec":"Oncology","min":30000,"max":150000,"days":1,"keywords":["cancer","chemo","chemotherapy","tumor","blood cancer","breast cancer"],"desc":"Systemic chemotherapy treatment cycle"},
    {"id":12,"name":"Kidney Dialysis (per session)","spec":"Nephrology","min":2000,"max":8000,"days":1,"keywords":["dialysis","kidney failure","kidney disease","renal failure"],"desc":"Haemodialysis for end-stage renal disease"},
    {"id":13,"name":"Cardiac Angiography","spec":"Cardiology","min":15000,"max":40000,"days":1,"keywords":["angiography","heart test","angio","angiogram"],"desc":"Coronary angiography with contrast"},
    {"id":14,"name":"Normal Delivery","spec":"Gynecology","min":20000,"max":60000,"days":3,"keywords":["delivery","pregnancy","normal delivery","labour","prasav"],"desc":"Assisted normal vaginal childbirth"},
    {"id":15,"name":"Caesarean Section","spec":"Gynecology","min":60000,"max":180000,"days":5,"keywords":["caesarean","c-section","cesarean","delivery operation"],"desc":"Surgical childbirth procedure"},
    {"id":16,"name":"Liver Transplant","spec":"Transplant","min":1500000,"max":3000000,"days":30,"keywords":["liver transplant","liver failure","cirrhosis","liver"],"desc":"Orthotopic liver transplantation"},
    {"id":17,"name":"Pacemaker Implantation","spec":"Cardiology","min":180000,"max":450000,"days":3,"keywords":["pacemaker","heart rate slow","cardiac pacemaker","bradycardia"],"desc":"Permanent cardiac pacemaker implantation"},
    {"id":18,"name":"Diabetic Foot Surgery","spec":"Vascular Surgery","min":80000,"max":250000,"days":7,"keywords":["diabetic foot","foot ulcer","diabetes foot","gangrene"],"desc":"Surgical treatment for diabetic foot complications"},
]

SYMPTOM_MAP = {
    "chest pain":    {"condition":"Coronary Artery Disease","proc_ids":[1,2,13],"urgency":"high","icon":"❤️"},
    "heart attack":  {"condition":"Acute Myocardial Infarction","proc_ids":[1,2],"urgency":"emergency","icon":"🚨"},
    "cardiac":       {"condition":"Cardiac Condition","proc_ids":[1,13],"urgency":"high","icon":"❤️"},
    "bypass":        {"condition":"Coronary Artery Disease (Severe)","proc_ids":[2],"urgency":"high","icon":"❤️"},
    "angioplasty":   {"condition":"Coronary Artery Disease","proc_ids":[1],"urgency":"high","icon":"❤️"},
    "angiography":   {"condition":"Suspected CAD","proc_ids":[13],"urgency":"medium","icon":"❤️"},
    "pacemaker":     {"condition":"Cardiac Arrhythmia","proc_ids":[17],"urgency":"high","icon":"💓"},
    "knee pain":     {"condition":"Knee Osteoarthritis","proc_ids":[3],"urgency":"low","icon":"🦵"},
    "knee":          {"condition":"Knee Disorder","proc_ids":[3],"urgency":"low","icon":"🦵"},
    "hip pain":      {"condition":"Hip Osteoarthritis","proc_ids":[4],"urgency":"low","icon":"🦴"},
    "brain tumor":   {"condition":"Brain Tumor","proc_ids":[5],"urgency":"high","icon":"🧠"},
    "appendix":      {"condition":"Appendicitis","proc_ids":[6],"urgency":"high","icon":"🤕"},
    "appendicitis":  {"condition":"Appendicitis","proc_ids":[6],"urgency":"high","icon":"🤕"},
    "cataract":      {"condition":"Cataract","proc_ids":[7],"urgency":"low","icon":"👁️"},
    "motiyabind":    {"condition":"Cataract (मोतियाबिंद)","proc_ids":[7],"urgency":"low","icon":"👁️"},
    "kidney stone":  {"condition":"Nephrolithiasis","proc_ids":[8],"urgency":"medium","icon":"🫘"},
    "pathri":        {"condition":"Kidney Stone (पथरी)","proc_ids":[8],"urgency":"medium","icon":"🫘"},
    "kidney failure":{"condition":"Chronic Kidney Disease","proc_ids":[12],"urgency":"high","icon":"🫘"},
    "dialysis":      {"condition":"Renal Failure","proc_ids":[12],"urgency":"high","icon":"🫘"},
    "gallbladder":   {"condition":"Cholelithiasis","proc_ids":[9],"urgency":"medium","icon":"🫀"},
    "back pain":     {"condition":"Lumbar Disc Disease","proc_ids":[10],"urgency":"medium","icon":"🦴"},
    "slip disc":     {"condition":"Herniated Disc","proc_ids":[10],"urgency":"medium","icon":"🦴"},
    "sciatica":      {"condition":"Sciatica","proc_ids":[10],"urgency":"medium","icon":"🦴"},
    "cancer":        {"condition":"Malignancy","proc_ids":[11],"urgency":"high","icon":"🔴"},
    "pregnancy":     {"condition":"Pregnancy","proc_ids":[14,15],"urgency":"medium","icon":"🤰"},
    "delivery":      {"condition":"Childbirth","proc_ids":[14,15],"urgency":"medium","icon":"🤰"},
    "liver":         {"condition":"Liver Disease","proc_ids":[16],"urgency":"high","icon":"🫁"},
    "cirrhosis":     {"condition":"Liver Cirrhosis","proc_ids":[16],"urgency":"high","icon":"🫁"},
    "diabetic foot": {"condition":"Diabetic Foot Complications","proc_ids":[18],"urgency":"high","icon":"🦶"},
    "gangrene":      {"condition":"Gangrene","proc_ids":[18],"urgency":"emergency","icon":"🚨"},
}

CITY_MULT = {
    "mumbai":1.4,"delhi":1.35,"bangalore":1.3,"bengaluru":1.3,"chennai":1.25,
    "hyderabad":1.2,"kolkata":1.15,"pune":1.2,"ahmedabad":1.1,"jaipur":1.0,
    "nagpur":1.0,"lucknow":0.95,"coimbatore":0.95,"bhopal":0.9,"visakhapatnam":0.9,
    "indore":0.9,"patna":0.85,"ranchi":0.85,"guwahati":0.85,"vellore":0.9,
    "surat":1.05,"kochi":1.0,"chandigarh":1.05
}

INSURANCE_DB = [
    {"id":"pmjay","name":"Ayushman Bharat PM-JAY","type":"government","coverage":500000,"premium":0,
     "note":"Free for eligible BPL families. Covers 1949+ medical packages.","phone":"14555",
     "website":"https://pmjay.gov.in","eligibility":"BPL families, SECC database listed",
     "benefits":["₹5 lakh cover per family per year","No premium","Cashless at empanelled hospitals","Pre-existing covered from Day 1"]},
    {"id":"star","name":"Star Health Insurance","type":"private","coverage":1000000,"premium":15000,
     "note":"Cashless at 14,000+ hospitals. Wide coverage.","phone":"1800-425-2255",
     "website":"https://www.starhealth.in","eligibility":"Age 18-65 years",
     "benefits":["₹10 lakh family floater","14,000+ cashless hospitals","No co-pay","Mental health cover"]},
    {"id":"hdfc","name":"HDFC ERGO Health (Optima Restore)","type":"private","coverage":1500000,"premium":18000,
     "note":"Auto-restore benefit after exhaustion.","phone":"1800-2700-700",
     "website":"https://www.hdfcergo.com","eligibility":"Age 5-65 years",
     "benefits":["₹15 lakh with auto-restore","13,000+ hospitals","No sub-limits","AYUSH cover"]},
    {"id":"national","name":"National Mediclaim Policy","type":"government","coverage":500000,"premium":8000,
     "note":"Government backed. Tax benefit under 80D.","phone":"1800-209-1415",
     "website":"https://www.nationalinsuranceindia.nic.co.in","eligibility":"Any Indian 18-65",
     "benefits":["₹5 lakh cover","Government-backed","Tax benefit 80D","Critical illness"]},
    {"id":"esic","name":"ESIC (Employees' State Insurance)","type":"government","coverage":1000000,"premium":0,
     "note":"For salaried employees ≤ ₹21,000/month. Employer-funded.","phone":"1800-11-2526",
     "website":"https://www.esic.in","eligibility":"Salaried employees ≤ ₹21,000/month",
     "benefits":["Full medical for employee & family","No employee premium","Maternity/disability benefits","Free medicines"]},
]

# ─────────────────────────────────────────────
# NLP ENGINE
# ─────────────────────────────────────────────

def detect_language(text: str) -> str:
    devanagari = sum(1 for c in text if '\u0900' <= c <= '\u097F')
    tamil = sum(1 for c in text if '\u0B80' <= c <= '\u0BFF')
    telugu = sum(1 for c in text if '\u0C00' <= c <= '\u0C7F')
    bengali = sum(1 for c in text if '\u0980' <= c <= '\u09FF')
    scores = {"hi": devanagari, "ta": tamil, "te": telugu, "bn": bengali}
    max_lang = max(scores, key=scores.get)
    return max_lang if scores[max_lang] > 0 else "en"

def extract_budget(text: str):
    text_lower = text.lower()
    lakh_m = re.search(r'(\d+(?:\.\d+)?)\s*(?:lakh|lac|लाख|லட்சம்|లక్ష)', text_lower)
    if lakh_m: return int(float(lakh_m.group(1)) * 100000)
    crore_m = re.search(r'(\d+(?:\.\d+)?)\s*(?:crore|cr|करोड़)', text_lower)
    if crore_m: return int(float(crore_m.group(1)) * 10000000)
    num_m = re.search(r'(?:rs\.?|₹|inr)?\s*(\d[\d,]+)', text_lower)
    if num_m: return int(num_m.group(1).replace(',', ''))
    return None

def extract_location(text: str):
    cities = list(CITY_MULT.keys()) + ["mumbai","delhi","bangalore","bengaluru","chennai","hyderabad","kolkata","pune","ahmedabad","jaipur","nagpur","lucknow","coimbatore","bhopal","visakhapatnam","indore","surat","kochi","chandigarh","vellore","patna","ranchi","guwahati","amritsar","varanasi","agra","noida","gurugram","faridabad","meerut","ghaziabad","bhubaneswar","thiruvananthapuram"]
    text_lower = text.lower()
    for city in cities:
        if city in text_lower:
            return city.title()
    return None

def estimate_cost(procedure: dict, city: str, age: int = 45, comorbidities: list = []) -> dict:
    city_factor = CITY_MULT.get(city.lower(), 1.0)
    risk = 1 + (0.08 * len(comorbidities))
    age_factor = 1.0 + (0.01 * max(0, age - 40))
    total_min = int(procedure["min"] * city_factor * risk * age_factor)
    total_max = int(procedure["max"] * city_factor * risk * age_factor)
    return {
        "total_min": total_min,
        "total_max": total_max,
        "formatted_min": f"₹{total_min:,}",
        "formatted_max": f"₹{total_max:,}",
        "breakdown": {
            "procedure": int(procedure["min"] * 0.55 * city_factor),
            "hospital_stay": int(procedure["min"] * 0.20 * city_factor),
            "diagnostics": int(procedure["min"] * 0.10 * city_factor),
            "medicines": int(procedure["min"] * 0.08 * city_factor),
            "nursing": int(procedure["min"] * 0.05 * city_factor),
            "contingency": int(procedure["min"] * 0.02 * city_factor),
        },
        "city_multiplier": city_factor,
        "risk_factor": round(risk, 2),
    }

def rank_hospitals(hospitals, procedure, budget, user_city):
    results = []
    for h in hospitals:
        cost = estimate_cost(procedure, h["city"])
        has_spec = "All Specialties" in h.get("specializations", []) or any(
            procedure["spec"].lower().split()[0] in s.lower() for s in h.get("specializations", []))
        clin = 1.0 if has_spec else 0.5
        budget_fit = 1.0
        if budget:
            mid = (cost["total_min"] + cost["total_max"]) / 2
            budget_fit = min(1.0, budget/mid*0.5) if mid <= budget else max(0.1, 1-(mid-budget)/budget)
        nearby = 1.0 if h["city"].lower() == user_city.lower() else 0.3
        score = 0.40*clin + 0.30*budget_fit + 0.20*(h["rating"]/5.0) + 0.10*nearby
        tags = []
        if h["cost_index"] == "low": tags.append("💰 Budget Friendly")
        if h["rating"] >= 4.5: tags.append("⭐ Top Rated")
        if h["type"] == "government": tags.append("🏛️ Government")
        if "JCI" in h.get("accreditation", ""): tags.append("🌟 JCI Accredited")
        if h.get("emergency"): tags.append("🚑 24/7 Emergency")
        results.append({**h, "score": round(score, 3), "cost_estimate": cost, "tags": tags[:4]})
    return sorted(results, key=lambda x: x["score"], reverse=True)

# ─────────────────────────────────────────────
# API ROUTES
# ─────────────────────────────────────────────

class QueryRequest(BaseModel):
    query: str
    language: Optional[str] = "auto"
    age: Optional[int] = 45
    comorbidities: Optional[List[str]] = []
    name: Optional[str] = ""
    budget: Optional[int] = None

@app.get("/")
async def root():
    return {"status": "JeevanCare API running", "version": "2.0.0", "tagline": "Empowering India with Intelligent Care"}

@app.get("/api/health")
async def health():
    return {"status": "ok", "hospitals": len(HOSPITALS_DB), "procedures": len(PROCEDURES_DB)}

@app.post("/api/query")
async def process_query(req: QueryRequest):
    try:
        query_lower = req.query.lower()
        lang = detect_language(req.query) if req.language == "auto" else req.language
        location = extract_location(query_lower)
        budget = req.budget or extract_budget(query_lower)

        # Match symptom
        condition = None
        proc_ids = []
        urgency = "medium"
        icon = "🩺"
        for kw, data in SYMPTOM_MAP.items():
            if kw in query_lower:
                condition = data["condition"]
                proc_ids = data["proc_ids"]
                urgency = data["urgency"]
                icon = data["icon"]
                if data["urgency"] in ("emergency", "high"):
                    break

        if not condition:
            for proc in PROCEDURES_DB:
                for kw in proc["keywords"]:
                    if kw in query_lower:
                        condition = f"Requires {proc['name']}"
                        proc_ids = [proc["id"]]
                        break
                if proc_ids:
                    break

        if not condition:
            return {"success": False, "hint": True, "message": "Please describe your symptoms more clearly, e.g. 'chest pain Mumbai ₹3 lakh' or 'knee pain Delhi age 55'."}

        procedure = next((p for p in PROCEDURES_DB if p["id"] == proc_ids[0]), None)
        if not procedure:
            return {"success": False, "hint": True, "message": "Procedure not found in database."}

        # Hospital pool
        pool = HOSPITALS_DB.copy()
        if location:
            city_hosps = [h for h in pool if h["city"].lower() == location.lower()]
            if len(city_hosps) < 3:
                pool = city_hosps + [h for h in pool if h["city"].lower() != location.lower()][:8]
            else:
                pool = city_hosps

        ranked = rank_hospitals(pool[:12], procedure, budget, location or "Mumbai")[:5]
        cost = estimate_cost(procedure, location or "Mumbai", req.age or 45, req.comorbidities or [])

        city_mult = CITY_MULT.get((location or "Mumbai").lower(), 1.0)
        market_avg = int((procedure["min"] + procedure["max"]) / 2 * city_mult)
        diff_pct = round(((cost["total_min"] - market_avg) / market_avg) * 100, 1)
        fairness_status = "🟢 Great Value" if diff_pct <= -15 else "🟢 Fair" if diff_pct <= 5 else "🟡 Slightly High" if diff_pct <= 20 else "🔴 Premium"

        conf = 0.0
        if condition: conf += 0.30
        if location: conf += 0.25
        if budget: conf += 0.20
        if len(ranked) >= 3: conf += 0.15
        conf += 0.10

        insurance = [i for i in INSURANCE_DB if i["coverage"] >= cost["total_min"] * 0.5][:3]

        return {
            "success": True,
            "language": lang,
            "condition": condition,
            "icon": icon,
            "urgency": urgency,
            "procedure": procedure,
            "hospitals": ranked,
            "cost_estimate": cost,
            "fairness": {"market_avg": market_avg, "diff_pct": diff_pct, "status": fairness_status},
            "confidence": {"score": round(conf, 2), "percentage": int(conf * 100), "level": "High" if conf >= 0.7 else "Medium" if conf >= 0.45 else "Low"},
            "insurance": insurance,
            "query_analysis": {"location": location, "budget": budget, "condition": condition},
            "disclaimer": "⚠️ This is decision-support only. Always consult a qualified doctor.",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hospitals")
async def get_hospitals(city: Optional[str] = None, specialization: Optional[str] = None):
    result = HOSPITALS_DB.copy()
    if city:
        result = [h for h in result if city.lower() in h["city"].lower()]
    if specialization:
        result = [h for h in result if any(specialization.lower() in s.lower() for s in h.get("specializations", []))]
    return {"hospitals": result, "count": len(result)}

@app.get("/api/procedures")
async def get_procedures(search: Optional[str] = None):
    result = PROCEDURES_DB.copy()
    if search:
        result = [p for p in result if search.lower() in p["name"].lower() or any(search.lower() in k for k in p.get("keywords", []))]
    return {"procedures": result, "count": len(result)}

@app.get("/api/insurance")
async def get_insurance(min_coverage: Optional[int] = None):
    result = INSURANCE_DB.copy()
    if min_coverage:
        result = [i for i in result if i["coverage"] >= min_coverage]
    return {"schemes": result, "count": len(result)}

@app.get("/api/cities")
async def get_cities():
    cities = sorted(set(h["city"] for h in HOSPITALS_DB))
    return {"cities": cities}

@app.get("/api/fun-fact")
async def get_fun_fact():
    facts = [
        "❤️ Your heart beats ~100,000 times a day — more dedication than most gym-goers!",
        "🧠 Your brain is 73% water. Staying hydrated literally helps you think better!",
        "😴 You'll spend 1/3 of your life sleeping. The other 2/3 Googling symptoms at 2 AM.",
        "🦠 Your gut has more bacteria than stars in the Milky Way — working overtime!",
        "🤧 A sneeze travels at 160 km/h — faster than most Indian trains!",
        "💉 Ayushman Bharat has helped 30+ crore Indians access free healthcare since 2018.",
        "🏥 India has 7.5 lakh+ beds in government hospitals. Knowing where to go saves lives!",
        "🌿 India's AYUSH system covers Ayurveda, Yoga, Naturopathy, Unani, Siddha & Homeopathy.",
    ]
    return {"fact": random.choice(facts)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
