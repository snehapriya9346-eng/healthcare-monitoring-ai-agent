# 🏥 HealthAI: Family Healthcare Monitoring Dashboard

An elegant, secure, and standalone relational healthcare analytics platform built using Python, Streamlit, and SQLite3. This application serves as a dedicated digital assistant to monitor physical vital signs, track chronological wellness metrics, and manage daily prescription logs seamlessly across family user profiles.

---

## 🌟 Core Implementation Features

- **Multi-Patient User Management Profile**
  - Features a responsive, stateful application canvas allowing examiners to fluidly jump between loaded family directory profiles (e.g., `sneha`, `sanju`, `Anita`) via sidebar interactive controls.
- **Robust SQLite3 Relational Architecture**
  - Built upon a clean relational data mapping layer with rigorous Foreign Key constraints, maintaining perfect data integrity and enabling zero-redundancy indexing.
- **Vitals Visual Analytics Engine**
  - Synthesizes and plots historical clinical parameters (including Daily Steps, Burned Calories, and Sleep Hours) on timeline graphs leveraging the `matplotlib` visualization runtime.
- **Automated Vitals Data Simulator**
  - Features an embedded health-metrics generator engine capable of populating randomized, standard biometric data for responsive local presentation testing.
- **Clinical Medication Tracker**
  - Provides instant structured visibility into prescription inventory logs, displaying active medical names, specialized unit dosages, and daily time schedules.

---

## 📊 Relational Database Schema Design

The engine orchestrates data across 3 strictly mapped tables managed within a localized instance (`health.db`):

1. `patients`: The parent entity structural lookup table mapping individual client keys (`patient_name`).
2. `medications`: Anchors custom pharmaceutical configurations directly back to a profile identity using an explicit `FOREIGN KEY (patient_name) REFERENCES patients` configuration with automated cascading deletions.
3. `health_metrics`: Aggregates temporal health indicators including logging date records, physical activity variables (`steps`, `calories`), sleep lengths, and automated vascular trends (`systolic`, `diastolic`, `heart_rate`).

---

## 🛠️ Complete Project Dependency Stack

- **UI Interface Render Engine**: `Streamlit`
- **Data Engineering Layer**: `Pandas`
- **Plotting & Analytics Engine**: `Matplotlib`
- **Relational Backend Environment**: `SQLite3`

---

## 🚀 Step-by-Step Environment Setup

1. **Bootstrap Core Matrix**: Execute the environment setup cell to install runtime requirements and dependencies.
2. **Compile Application Infrastructure**: Run the target schema scripts to write out structural assets, formulate database tables, and insert pre-loaded validation samples.
3. **Launch Live Deployment Link**: Fire up the local server script using Colab's internal secure proxy method to immediately render the operational web application on your dashboard screen.
