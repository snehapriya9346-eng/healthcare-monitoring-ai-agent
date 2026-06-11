import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import random
import requests
import xml.etree.ElementTree as ET
from datetime import date

st.set_page_config(page_title="Healthcare Monitoring AI Agent", layout="wide")

# ---------- Database Helpers ----------
def get_db_connection():
    conn = sqlite3.connect("health.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT UNIQUE NOT NULL,
            age INTEGER,
            gender TEXT,
            medical_history TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            medicine_name TEXT,
            dosage TEXT,
            time_str TEXT,
            FOREIGN KEY (patient_name) REFERENCES patients (patient_name)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def fake_health_metrics():
    return (random.randint(2000, 9000),
            random.randint(1500, 2600),
            round(random.uniform(4.0, 8.0), 1))

def get_meds(patient_name):
    conn = get_db_connection()
    df = pd.read_sql_query(
        "SELECT medicine_name, dosage, time_str FROM medications WHERE patient_name = ?",
        conn, params=(patient_name,))
    conn.close()
    return df

def all_patients():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT DISTINCT patient_name FROM patients", conn)
    conn.close()
    p_list = df["patient_name"].tolist()
    return p_list if p_list else ["Demo Patient"]

def check_interactions(meds):
    risky_pairs = {
        ("Paracetamol", "Ibuprofen"): "Use cautiously together; consult a doctor.",
        ("Metformin", "Alcohol"): "Can increase risk of lactic acidosis.",
        ("Aspirin", "Warfarin"): "High Risk: Increased bleeding tendency.",
        ("Ibuprofen", "Aspirin"): "Moderate Risk: Decreased aspirin efficacy.",
        ("Amlodipine", "Simvastatin"): "Mild Risk: Increased simvastatin exposure."
    }
    found = []
    names = [m.lower().strip() for m in meds]
    for (a, b), msg in risky_pairs.items():
        if a.lower() in names and b.lower() in names:
            found.append(f"⚠️ **{a} + {b}**: {msg}")
    return found

# ---------- UI Layout ----------
st.title("🏥 Healthcare Monitoring AI Agent")

menu = st.sidebar.selectbox("Navigation Menu", 
    ["Patient Registration", "Dashboard & Vitals", "Clinical Analysis", "MedlinePlus Search", "Export Reports"])

# ---------- Menu 1: Patient Registration ----------
if menu == "Patient Registration":
    st.subheader("📝 Register New Patient Profile")
    with st.form("reg_form", clear_on_submit=True):
        p_name = st.text_input("Patient Full Name")
        p_age = st.number_input("Age", min_value=0, max_value=120, value=25)
        p_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        p_history = st.text_area("Past Medical History")
        submit = st.form_submit_button("Save Patient Profile")
        
        if submit and p_name:
            try:
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("INSERT INTO patients (patient_name, age, gender, medical_history) VALUES (?, ?, ?, ?)",
                          (p_name, p_age, p_gender, p_history))
                conn.commit()
                conn.close()
                st.success(f"Successfully registered profile for {p_name}!")
            except sqlite3.IntegrityError:
                st.warning("This patient name is already registered.")

# ---------- Universal Patient Selector for remaining tabs ----------
else:
    plist = all_patients()
    patient = st.sidebar.selectbox("Select Active Patient Profile", plist)
    
    # Load profile details
    conn = get_db_connection()
    profile = conn.execute("SELECT * FROM patients WHERE patient_name = ?", (patient,)).fetchone()
    conn.close()

    # ---------- Menu 2: Dashboard & Vitals ----------
    if menu == "Dashboard & Vitals":
        st.subheader(f"📊 Health Analytics — {patient}")
        if profile:
            st.markdown(f"**Age:** {profile['age']} | **Gender:** {profile['gender']}")
            st.markdown(f"**Medical History:** {profile['medical_history'] if profile['medical_history'] else 'None reported'}")
        
        steps, calories, sleep_hours = fake_health_metrics()
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Daily Steps 🏃‍♂️", f"{steps} steps")
        metric_col2.metric("Calories Burned 🔥", f"{calories} kcal")
        metric_col3.metric("Sleep Duration 😴", f"{sleep_hours} hrs")
        
        # Side-by-Side Grid Layout for Trends
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("#### Blood Pressure Trends")
            bp_df = pd.DataFrame({
                "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "Systolic": [random.randint(115, 130) for _ in range(7)],
                "Diastolic": [random.randint(75, 85) for _ in range(7)]
            }).set_index("Day")
            st.line_chart(bp_df)
            
        with chart_col2:
            st.markdown("#### Heart Rate History (BPM)")
            hr_df = pd.DataFrame({
                "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "Heart Rate": [random.randint(68, 88) for _ in range(7)]
            }).set_index("Day")
            st.line_chart(hr_df)

    # ---------- Menu 3: Clinical Analysis ----------
    elif menu == "Clinical Analysis":
        st.subheader(f"🩺 Smart Diagnostics & Logs — {patient}")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### Log New Medication")
            with st.form("med_form", clear_on_submit=True):
                med_name = st.text_input("Medicine Name (e.g., Paracetamol, Metformin, Aspirin, Ibuprofen)")
                dosage = st.text_input("Dosage Description (e.g., 500mg, Twice daily)")
                time_str = st.text_input("Schedule Time (e.g., 08:00 AM)")
                add_med = st.form_submit_button("Log Medication")
                
                if add_med and med_name:
                    conn = get_db_connection()
                    c = conn.cursor()
                    # Ensure patient profile scaffold exists
                    c.execute("INSERT OR IGNORE INTO patients (patient_name, age, gender, medical_history) VALUES (?, 25, 'Other', '')", (patient,))
                    c.execute("INSERT INTO medications (patient_name, medicine_name, dosage, time_str) VALUES (?, ?, ?, ?)",
                              (patient, med_name, dosage, time_str))
                    conn.commit()
                    conn.close()
                    st.success(f"Added {med_name} to profile database logs.")
            
            st.markdown("#### Current Medication Schedule")
            meds_df = get_meds(patient)
            if not meds_df.empty:
                st.dataframe(meds_df, use_container_width=True)
                # Check for warnings
                warnings = check_interactions(meds_df["medicine_name"].tolist())
                if warnings:
                    for w in warnings:
                        st.warning(w)
                else:
                    st.info("✅ No conflicting interactions detected in logged medication pair database.")
            else:
                st.info("No active medications logged for this profile.")

        with col_right:
            st.markdown("#### Evaluate Clinical Inputs")
            symptoms = st.text_area("Current Symptoms Box")
            vitals_text = st.text_area("Manual Vitals Data (e.g., BP: 120/80, SpO2: 98%)")
            
            if st.button("Analyze and Recommend"):
                with st.spinner("Analyzing patient data..."):
                    text = symptoms.lower()

                    if "fever" in text and "cough" in text:
                        diagnosis = "Possible upper respiratory infection."
                        treatment = (
                            "Encourage rest, warm fluids, steam inhalation, and paracetamol for fever. "
                            "Consult a doctor if symptoms persist beyond 3–5 days, breathing difficulty, or chest pain occurs."
                        )

                    elif "fever" in text and "vomiting" in text:
                        diagnosis = "Possible gastrointestinal infection."
                        treatment = (
                            "Oral rehydration solution (ORS), light diet, and paracetamol for fever. "
                            "Consult a doctor if vomiting is persistent, blood is seen, or there are signs of dehydration."
                        )

                    elif "chest pain" in text:
                        diagnosis = "Chest pain reported – potentially serious."
                        treatment = (
                            "Immediate medical evaluation is recommended. Avoid self‑medication. "
                            "If chest pain is severe, radiating, or associated with sweating or breathlessness, seek emergency care."
                        )

                    elif "shortness of breath" in text or "breathlessness" in text:
                        diagnosis = "Breathing difficulty reported."
                        treatment = (
                            "This can be serious. The patient should be evaluated urgently by a healthcare professional. "
                            "If severe, go to the nearest emergency facility."
                        )

                    elif "headache" in text and "vision" in text:
                        diagnosis = "Headache with visual symptoms."
                        treatment = (
                            "May be migraine or other neurological condition. Rest in a dark room, hydration, and simple analgesics may help, "
                            "but consult a doctor, especially if new, severe, or associated with weakness or confusion."
                        )

                    elif "diabetes" in text or "sugar" in text:
                        diagnosis = "History or suspicion of diabetes."
                        treatment = (
                            "Advise regular blood sugar monitoring, dietary control, exercise, and adherence to prescribed medication. "
                            "Consult a doctor for medication adjustment and complication screening."
                        )

                    elif "hypertension" in text or "high bp" in text or "high blood pressure" in text:
                        diagnosis = "History or suspicion of hypertension."
                        treatment = (
                            "Recommend regular BP monitoring, reduced salt intake, stress management, and adherence to antihypertensive medication. "
                            "Consult a doctor for proper evaluation and follow‑up."
                        )

                    elif "fever" in text:
                        diagnosis = "Possible infection with fever."
                        treatment = (
                            "Hydration, rest, and paracetamol as needed (as per dose). "
                            "Consult a doctor if symptoms persist beyond 3 days or worsen."
                        )

                    else:
                        diagnosis = "No specific condition detected from the given symptoms."
                        treatment = (
                            "Monitor symptoms, maintain hydration and rest, and consult a healthcare professional for proper evaluation."
                        )

                st.subheader("Preliminary Diagnosis")
                st.write(diagnosis)
                st.subheader("Suggested Treatment Plan")
                st.write(treatment)

    # ---------- Menu 4: MedlinePlus Search ----------
    elif menu == "MedlinePlus Search":
        st.subheader("🔍 MedlinePlus Trusted Web Reference Lookup")
        query = st.text_input("Enter condition or keyword (e.g., Hypertension, Diabetes):", "Hypertension")
        if st.button("Search MedlinePlus"):
            try:
                fallback_url = f"https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term={query}"
                res = requests.get(fallback_url)
                root = ET.fromstring(res.content)
                docs = root.findall(".//document")
                if not docs:
                    st.info("No matching web results found.")
                for doc in docs[:4]:
                    url_attr = doc.attrib.get("url", "#")
                    title = "Medical Article Reference"
                    for c in doc.findall("content"):
                        if c.attrib.get("name") == "title":
                            title = c.text or title
                    st.markdown(f"- [{title}]({url_attr})")
                st.caption("Source information extracted live from MedlinePlus (U.S. National Library of Medicine)")
            except Exception as e:
                st.error(f"Live medical verification service unavailable: {e}")

    # ---------- Menu 5: Export Reports ----------
    elif menu == "Export Reports":
        st.subheader(f"📥 Export Diagnostics Report — {patient}")
        steps, calories, sleep_hours = fake_health_metrics()
        meds = get_meds(patient)
        report = (f"HEALTH RECORD REPORT SUMMARY: {patient}\n"
                  f"Report Generation Date: {date.today().strftime('%Y-%m-%d')}\n"
                  f"{'='*40}\n"
                  f"Activity Metrics:\n"
                  f"  - Calculated Day Steps: {steps}\n"
                  f"  - Active Calorie Burn: {calories} kcal\n"
                  f"  - Tracked Sleep: {sleep_hours} Hours\n\n"
                  f"Active Logged Medications:\n" +
                  ("\n".join(f"  * {r.medicine_name} ({r.dosage}) Scheduled: {r.time_str}"
                            for r in meds.itertuples()) or "  No recorded logs.")
                  )
        st.text(report)
        st.download_button("⬇️ Download Patient Report Summary (.txt)", report,
                           file_name=f"{patient.replace(' ', '_')}_health_report.txt")

st.markdown("---")
st.caption("Disclaimer: This tool is for educational purposes only and not a substitute for professional medical advice.")
