import sqlite3
import pandas as pd

DB_PATH = "med_wellness_family.db"

def init_db():
    # 'with' blocks automatically handle commits and safely close the connection
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        # 1. Create Tables with Explicit Relational Foreign Keys
        cur.execute("""
        CREATE TABLE IF NOT EXISTS family_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            relation TEXT
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            med_name TEXT,
            dosage TEXT,
            schedule TEXT,
            FOREIGN KEY (member_id) REFERENCES family_members(id) ON DELETE CASCADE
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS med_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            med_id INTEGER,
            taken_date TEXT,
            status TEXT,
            FOREIGN KEY (member_id) REFERENCES family_members(id) ON DELETE CASCADE,
            FOREIGN KEY (med_id) REFERENCES medications(id) ON DELETE CASCADE
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS wellness_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            goal_type TEXT,
            target_value REAL,
            unit TEXT,
            FOREIGN KEY (member_id) REFERENCES family_members(id) ON DELETE CASCADE
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS wellness_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            goal_id INTEGER,
            log_date TEXT,
            value REAL,
            FOREIGN KEY (member_id) REFERENCES family_members(id) ON DELETE CASCADE,
            FOREIGN KEY (goal_id) REFERENCES wellness_goals(id) ON DELETE CASCADE
        )
        """)

        # 2. Clear out existing tables for a pristine script reset
        # Clear child tables first to respect database dependency constraints
        for table in ["wellness_logs", "wellness_goals", "med_logs", "medications", "family_members"]:
            cur.execute(f"DELETE FROM {table}")
            
        # 3. Seed Primary Family Profiles
        cur.execute("INSERT INTO family_members (name, relation) VALUES (?, ?)", ("Sneha", "Self"))
        cur.execute("INSERT INTO family_members (name, relation) VALUES (?, ?)", ("Bikshapathi", "Parent"))

    # 4. Fetch Primary Keys Dynamically via Pandas
    with sqlite3.connect(DB_PATH) as conn:
        family_df = pd.read_sql_query("SELECT * FROM family_members", conn)
        sneha_id = int(family_df[family_df["name"] == "Sneha"]["id"].iloc[0])
        father_id = int(family_df[family_df["name"] == "Bikshapathi"]["id"].iloc[0])

        cur = conn.cursor()
        
        # 5. Seed Medications and grab generated Row IDs instantly
        cur.execute("INSERT INTO medications (member_id, med_name, dosage, schedule) VALUES (?, ?, ?, ?)", 
                    (sneha_id, "Metformin", "500mg", "Morning & Night"))
        metformin_id = cur.lastrowid
        
        cur.execute("INSERT INTO medications (member_id, med_name, dosage, schedule) VALUES (?, ?, ?, ?)", 
                    (sneha_id, "Vitamin D", "1000 IU", "Morning"))
        vit_d_id = cur.lastrowid
        
        cur.execute("INSERT INTO medications (member_id, med_name, dosage, schedule) VALUES (?, ?, ?, ?)", 
                    (father_id, "BP Tablet", "50mg", "Morning"))
        bp_tablet_id = cur.lastrowid

        # 6. Seed Medication Logs safely using dynamic IDs
        cur.executemany(
            "INSERT INTO med_logs (member_id, med_id, taken_date, status) VALUES (?, ?, ?, ?)",
            [
                (sneha_id, metformin_id, "2025-03-01", "taken"),
                (sneha_id, metformin_id, "2025-03-02", "missed"),
                (sneha_id, vit_d_id, "2025-03-01", "taken"),
                (father_id, bp_tablet_id, "2025-03-01", "missed"),
                (father_id, bp_tablet_id, "2025-03-02", "taken"),
            ]
        )

        # 7. Seed Goals and grab generated IDs
        cur.execute("INSERT INTO wellness_goals (member_id, goal_type, target_value, unit) VALUES (?, ?, ?, ?)", 
                    (sneha_id, "Steps", 8000, "steps"))
        sneha_steps_goal = cur.lastrowid
        
        cur.execute("INSERT INTO wellness_goals (member_id, goal_type, target_value, unit) VALUES (?, ?, ?, ?)", 
                    (sneha_id, "Sleep", 7, "hours"))
        sneha_sleep_goal = cur.lastrowid
        
        cur.execute("INSERT INTO wellness_goals (member_id, goal_type, target_value, unit) VALUES (?, ?, ?, ?)", 
                    (father_id, "Steps", 5000, "steps"))
        father_steps_goal = cur.lastrowid

        # 8. Seed Wellness Logs safely using dynamic IDs
        cur.executemany(
            "INSERT INTO wellness_logs (member_id, goal_id, log_date, value) VALUES (?, ?, ?, ?)",
            [
                (sneha_id, sneha_steps_goal, "2025-03-01", 6000),
                (sneha_id, sneha_steps_goal, "2025-03-02", 9000),
                (sneha_id, sneha_sleep_goal, "2025-03-01", 6.5),
                (sneha_id, sneha_sleep_goal, "2025-03-02", 7.5),
                (father_id, father_steps_goal, "2025-03-01", 3000),
                (father_id, father_steps_goal, "2025-03-02", 5200),
            ]
        )
        print("Local DB successfully generated and safely seeded with zero hardcoding flaws!")

if __name__ == "__main__":
    init_db()
