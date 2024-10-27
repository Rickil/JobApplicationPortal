# initialize_database.py

import sqlite3
import os

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)
os.makedirs('data/resumes', exist_ok=True)
os.makedirs('data/job_offers', exist_ok=True)

conn = sqlite3.connect('data/database.db')
c = conn.cursor()

# Create the job_offers table
c.execute('''
    CREATE TABLE IF NOT EXISTS job_offers (
        job_id TEXT PRIMARY KEY,
        title TEXT,
        required_skills TEXT
    )
''')

# Create the applicants table
c.execute('''
    CREATE TABLE IF NOT EXISTS applicants (
        applicant_id TEXT PRIMARY KEY,
        job_id TEXT,
        data TEXT,
        FOREIGN KEY(job_id) REFERENCES job_offers(job_id)
    )
''')

conn.commit()
conn.close()