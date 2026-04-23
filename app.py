import streamlit as st

def main():
    st.set_page_config(page_title="Healthcare Monitoring AI Agent", layout="wide")
    st.title("Healthcare Monitoring AI Agent")

    st.sidebar.header("Patient Information")

    name = st.sidebar.text_input("Patient Name")
    age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=25)
    gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])

    st.subheader("Clinical Inputs")
    symptoms = st.text_area("Current Symptoms")
    medical_history = st.text_area("Past Medical History")
    vitals = st.text_area("Vitals (e.g., BP: 120/80, HR: 82, SpO2: 98%)")

    if st.button("Analyze and Recommend"):
        with st.spinner("Analyzing patient data..."):
            # Simple placeholder logic (you can replace with AI later)
            if "fever" in symptoms.lower():
                diagnosis = "Possible infection with fever."
                treatment = "Hydration, rest, and paracetamol as needed. Consult a doctor if symptoms persist."
            else:
                diagnosis = "No specific condition detected from the given symptoms."
                treatment = "Monitor symptoms and consult a healthcare professional if needed."

        st.subheader("Preliminary Diagnosis")
        st.write(diagnosis)

        st.subheader("Suggested Treatment Plan")
        st.write(treatment)

    st.markdown("---")
    st.caption("Disclaimer: This tool is for educational purposes only and not a substitute for professional medical advice.")

if __name__ == "__main__":
    main()
