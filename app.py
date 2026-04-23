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
