# 🏥 JeevanCare – AI-Powered Healthcare Navigator & Cost Estimator

An intelligent healthcare decision-support platform that helps users identify potential medical conditions, estimate treatment costs, discover suitable hospitals, explore insurance options, and receive personalized healthcare guidance.

## 🚀 Features

### 🤖 AI-Powered Health Analysis

* Symptom-based disease prediction
* Personalized risk assessment
* Multilingual healthcare support
* Real-time condition analysis

### 🏥 Smart Hospital Recommendation

* Hospital ranking based on condition and budget
* Government and private hospital comparison
* Hospital contact details, website, and location support
* Accreditation and specialty-based filtering

### 💰 Treatment Cost Estimation

* Procedure-wise cost estimation
* Budget compatibility analysis
* Historical treatment cost insights
* Cost comparison across hospitals

### 🛡️ Insurance Assistance

* PM-JAY eligibility checking
* ESIC support information
* Private insurance guidance
* Step-by-step claim process explanation

### 📊 Healthcare Decision Support

* Treatment journey timeline
* Confidence score visualization
* Market fairness analysis
* Personalized recommendations based on age and medical history

### 🌐 Multilingual Support

* English
* Hindi
* Tamil
* Telugu
* Bengali
* Marathi

---

## 🏗️ Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* FastAPI

### Data Processing

* NLP-based symptom mapping
* Healthcare knowledge engine
* Hospital recommendation system

---

## 📂 Project Structure

```text
JeevanCare_Project/
│
├── frontend/
│   └── index.html
│
├── backend/
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/JeevanCare.git
cd JeevanCare_Project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Backend URL:

```text
http://localhost:8000
```

### 4. Launch Frontend

Open:

```text
frontend/index.html
```

in any modern web browser.

---

## 📡 API Endpoints

### Health Query

```http
POST /api/query
```

Analyze symptoms and receive healthcare recommendations.

### Hospital Search

```http
GET /api/hospitals
```

Retrieve recommended hospitals.

### Insurance Information

```http
GET /api/insurance
```

Access insurance schemes and eligibility information.

---

## 🏥 Supported Medical Conditions

* Heart Attack
* Chest Pain
* Knee Pain
* Hip Replacement
* Brain Tumor
* Kidney Stone
* Kidney Failure
* Appendicitis
* Gallbladder Disorders
* Cataract
* Cancer
* Pregnancy & Delivery
* Liver Disease
* Diabetic Foot
* Pacemaker Procedures
* Slip Disc & Back Pain

---

## 🌍 Supported Cities

* Mumbai
* Delhi
* Chennai
* Bangalore
* Hyderabad
* Kolkata
* Pune
* Ahmedabad
* Jaipur
* Lucknow
* Coimbatore
* Kochi
* Chandigarh
* Indore
* Surat
* Patna
* Ranchi
* Guwahati
* Visakhapatnam
* Vellore

---

## 🎯 Future Enhancements

* Integration with real hospital APIs
* Medical report upload and analysis
* AI chatbot for healthcare guidance
* Appointment booking system
* Voice-based symptom input
* Advanced predictive healthcare analytics

---

## 👩‍💻 Author

**Pooja KC**

AI & Data Science Undergraduate

Areas of Interest:

* Artificial Intelligence
* Machine Learning
* Deep Learning
* Natural Language Processing
* Computer Vision
* Generative AI

---

## 📜 License

This project is developed for educational, research, and innovation purposes.

**Disclaimer:** JeevanCare provides healthcare guidance and cost estimation only. It is not a substitute for professional medical diagnosis or treatment.
