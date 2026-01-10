# 🎒 TripMate for Campus  
## AI-Powered Travel Planner for College Students

---

## 📌 Project Overview

**TripMate for Campus** is an AI-powered travel planning application designed specifically for college students and educational institutions. The system automates **trip itinerary generation and budget estimation** by combining **Large Language Models (LLaMA 3.2)** with **rule-based cost calculations**.

The application enables users to generate a **day-wise itinerary**, **detailed budget breakdown**, **per-student cost analysis**, and **alternative budget options**, all through an interactive web interface.

---

## 🎯 Objectives

- Simplify college trip planning using AI  
- Generate structured and student-friendly itineraries  
- Calculate realistic and transparent trip budgets  
- Provide per-student cost clarity for fee collection  
- Enable downloadable reports for approvals and documentation  

---

## 🚀 Features

- AI-generated **day-wise itinerary** (Morning / Afternoon / Evening)
- Rule-based **transport, stay, food, and miscellaneous cost calculation**
- **Per-student cost transparency**
- **Alternative budget options** (Budget / Mid-range / Premium)
- Visual insights using **bar charts and pie charts**
- **PDF export** of itinerary and budget summary
- Interactive **Streamlit web interface**
- CPU-based inference (no GPU dependency)

---

## 🧠 System Architecture

- **Frontend:** Streamlit Web Interface  
- **Backend:** Python Logic + AI Inference  
- **AI Model:** LLaMA-3.2-3B-Instruct (via Hugging Face)  
- **Processing:** Pandas & rule-based algorithms  
- **Output:** Visual charts and PDF reports  

The system follows a **hybrid architecture**:
- AI-driven itinerary generation  
- Deterministic rule-based budgeting for accuracy  

---

## 🔍 Input Parameters

| Parameter | Type |
|---------|------|
| Starting Location | Text |
| Destination | Text |
| Travel Month | Dropdown (Categorical) |
| Number of Students | Integer |
| Number of Days | Integer |
| Preferred Location Types | Multi-select |
| Maximum Budget | Integer (₹) |

---

## ⚙️ Algorithm Overview

1. Collect user inputs through Streamlit form  
2. Generate itinerary using LLaMA 3.2 with prompt constraints  
3. Estimate distance using region-based logic  
4. Calculate transport cost based on group size  
5. Select stay type using student-count rules  
6. Compute food cost based on per-student budget  
7. Calculate miscellaneous cost using location types  
8. Compute total and per-student cost  
9. Generate alternative budget options  
10. Visualize results and export PDF reports  

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Hugging Face Transformers**
- **Pandas**
- **Matplotlib**
- **ReportLab**



## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/sinjumoncy/tripmate-for-campus.git
cd tripmate-for-campus
```
---
### 2 Edit the file
Open utils/ai_helper.py and replace the USE_THE_TRIPMATE_KEY with the key provided below it.

---
### 3. Run the app
To run the app on you terminal use the below
```bash
streamlit run app.py
```
---
### 👩‍💻 Developed By

#### ***Sinju Moncy***  

*TripMate for Campus was developed as an academic AI project focusing on practical problem-solving using Large Language Models and rule-based analytics.*




