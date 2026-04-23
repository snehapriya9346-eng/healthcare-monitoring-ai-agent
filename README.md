# HealthAI: Healthcare Monitoring AI Agent

A simple web-based healthcare assistant built with Python and Streamlit. The app allows users or caregivers to enter patient details (name, age, gender), symptoms, past medical history, and vital signs, and then generates a **preliminary diagnosis** and **suggested treatment plan** based on rule-based analysis of the symptoms.

> **Disclaimer:** This is an educational project, not medical advice. Always consult a qualified doctor before starting, stopping, or changing any treatment.

---

## Features

- **Patient data capture**
  - Patient name, age, gender
  - Current symptoms (free text)
  - Past medical history
  - Vitals (BP, heart rate, SpO2, etc.)

- **Preliminary diagnosis**
  - Uses simple rule-based logic on the symptom text.
  - Handles patterns such as:
    - Fever + cough → possible upper respiratory infection  
    - Fever + vomiting → possible gastrointestinal infection  
    - Chest pain → serious warning and advice for urgent evaluation  
    - Shortness of breath/breathlessness → urgent evaluation  
    - Headache with vision issues → possible migraine/neurological issue  
    - Diabetes / high sugar → diabetes-related advice  
    - Hypertension / high BP → blood pressure-related advice  
    - General case → “no specific condition detected” with safe advice

- **Suggested treatment plan**
  - High-level supportive care suggestions (rest, hydration, monitoring).
  - Always advises to consult a healthcare professional.

- **Simple, clean UI**
  - Built with Streamlit.
  - Runs in a web browser (no complex setup for users).

---

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Logic**: Rule-based symptom analysis (keyword matching)
- **Deployment**: Streamlit Cloud

---

## How to Run Locally

1. **Clone the repository**

   ```bash
   git clone https://github.com/snehapriya9346-eng/healthcare-monitoring-ai-agent.git
   cd healthcare-monitoring-ai-agent
   ```

2. **Create and activate a virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

5. Open the URL shown in the terminal (usually `http://localhost:8501`) in your browser.

---

## Live Demo

The app is deployed on Streamlit Community Cloud:

- **Live app:**  
  https://healthcare-monitoring-ai-agent-ewfkhlpg4rukk9mlpcthyf.streamlit.app/

---

## Architecture Overview

- **Input Layer (UI)**
  - Built with Streamlit.
  - Sidebar: patient demographics (name, age, gender).
  - Main area: clinical inputs (symptoms, history, vitals) and an **Analyze and Recommend** button.

- **Logic Layer**
  - Symptoms text is converted to lowercase.
  - A series of `if/elif` rules check for keywords:
    - `"fever"`, `"cough"`, `"vomiting"`, `"chest pain"`, `"shortness of breath"`, `"breathlessness"`, `"headache"`, `"vision"`, `"diabetes"`, `"sugar"`, `"hypertension"`, `"high bp"`, `"high blood pressure"`.
  - Based on the matched rule, the app sets:
    - `diagnosis` (Preliminary Diagnosis)
    - `treatment` (Suggested Treatment Plan)

- **Output Layer**
  - Displays:
    - **Preliminary Diagnosis**
    - **Suggested Treatment Plan**
  - Shows a disclaimer at the bottom.

---

## Future Work

- Replace rule-based logic with an AI/LLM model for more flexible and detailed reasoning.
- Connect to a medical knowledge base or guidelines.
- Add database support to store patient visit history.
- Extend to support IoT-based vitals monitoring (e.g., continuous BP/SpO2 from devices).

---

## Medical Safety Disclaimer

This project is intended **only for educational and academic purposes**.  
It is **not** a certified medical device or clinical decision support system.

- It does **not** provide professional medical advice.
- It should **not** be used to diagnose, treat, cure, or prevent any disease.
- Always consult a licensed doctor or qualified healthcare provider for real medical decisions.
