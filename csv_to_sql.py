import pandas as pd
import sqlite3
import os

# Read the CSV file
csv_file = 'fantasy_2025_full_weekly_with_positions.csv'
df = pd.read_csv(csv_file)

# Create SQLite database
db_file = 'fantasy_2025.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Drop table if it exists
cursor.execute('DROP TABLE IF EXISTS player_stats')

# Create table
cursor.execute('''
    CREATE TABLE player_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        position TEXT,
        week_1 REAL,
        week_2 REAL,
        week_3 REAL,
        week_4 REAL,
        week_5 REAL,
        week_6 REAL,
        week_7 REAL,
        week_8 REAL,
        week_9 REAL,
        week_10 REAL,
        week_11 REAL,
        week_12 REAL,
        week_13 REAL,
        total_points REAL
    )
''')

# Rename columns to be more compatible with SQL
df.columns = ['player_name', 'position'] + [f'week_{i}' for i in range(1, 14)] + ['total_points']

# Replace NaN with None so they insert as NULL
df = df.where(pd.notna(df), None)

# Insert data into database
for idx, row in df.iterrows():
    cursor.execute('''
        INSERT INTO player_stats 
        (player_name, position, week_1, week_2, week_3, week_4, week_5, week_6, week_7, 
         week_8, week_9, week_10, week_11, week_12, week_13, total_points)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(row))

conn.commit()
conn.close()

print(f"✓ Database created: {db_file}")
print(f"✓ Table: player_stats")
print(f"✓ Records inserted: {len(df)}")
print(f"\nDatabase file size: {os.path.getsize(db_file) / 1024:.2f} KB")
