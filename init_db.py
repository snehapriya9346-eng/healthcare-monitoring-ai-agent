import sqlite3
import pandas as pd

DB_PATH = "med_wellness_family.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS family_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    relation TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    med_name TEXT,
    dosage TEXT,
    schedule TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS med_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    med_id INTEGER,
    taken_date TEXT,
    status TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS wellness_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    goal_type TEXT,
    target_value REAL,
    unit TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS wellness_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    goal_id INTEGER,
    log_date TEXT,
    value REAL
)
""")

for table in ["family_members", "medications", "med_logs", "wellness_goals", "wellness_logs"]:
    cur.execute(f"DELETE FROM {table}")
conn.commit()

cur.execute("INSERT INTO family_members (name, relation) VALUES (?, ?)", ("Sneha", "Self"))
cur.execute("INSERT INTO family_members (name, relation) VALUES (?, ?)", ("Bikshapathi", "Parent"))
conn.commit()

family_df = pd.read_sql_query("SELECT * FROM family_members", conn)
print(family_df)

sneha_id = int(family_df[family_df["name"] == "Sneha"]["id"].iloc[0])
father_id = int(family_df[family_df["name"] == "Bikshapathi"]["id"].iloc[0])

cur.execute("INSERT INTO medications (member_id, med_name, dosage, schedule) VALUES (?, ?, ?, ?)",
            (sneha_id, "Metformin", "500mg", "Morning & Night"))
cur.execute("INSERT INTO medications (member_id, med_name, dosage, schedule) VALUES (?, ?, ?, ?)",
            (sneha_id, "Vitamin D", "1000 IU", "Morning"))
cur.execute("INSERT INTO medications (member_id, med_name, dosage, schedule) VALUES (?, ?, ?, ?)",
            (father_id, "BP Tablet", "50mg", "Morning"))
conn.commit()

cur.executemany(
    "INSERT INTO med_logs (member_id, med_id, taken_date, status) VALUES (?, ?, ?, ?)",
    [
        (sneha_id, 1, "2025-03-01", "taken"),
        (sneha_id, 1, "2025-03-02", "missed"),
        (sneha_id, 2, "2025-03-01", "taken"),
        (father_id, 3, "2025-03-01", "missed"),
        (father_id, 3, "2025-03-02", "taken"),
    ]
)

cur.execute("INSERT INTO wellness_goals (member_id, goal_type, target_value, unit) VALUES (?, ?, ?, ?)",
            (sneha_id, "Steps", 8000, "steps"))
cur.execute("INSERT INTO wellness_goals (member_id, goal_type, target_value, unit) VALUES (?, ?, ?, ?)",
            (sneha_id, "Sleep", 7, "hours"))
cur.execute("INSERT INTO wellness_goals (member_id, goal_type, target_value, unit) VALUES (?, ?, ?, ?)",
            (father_id, "Steps", 5000, "steps"))
conn.commit()

cur.executemany(
    "INSERT INTO wellness_logs (member_id, goal_id, log_date, value) VALUES (?, ?, ?, ?)",
    [
        (sneha_id, 1, "2025-03-01", 6000),
        (sneha_id, 1, "2025-03-02", 9000),
        (sneha_id, 2, "2025-03-01", 6.5),
        (sneha_id, 2, "2025-03-02", 7.5),
        (father_id, 3, "2025-03-01", 3000),
        (father_id, 3, "2025-03-02", 5200),
    ]
)
conn.commit()
conn.close()

print("Local DB ready with Sneha and Bikshapathi.")