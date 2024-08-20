import sqlite3

# # Database file path
DATABASE = 'insurance_claims.db'

# Function to create tables
def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Table for claims data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            months_as_customer INTEGER,
            age INTEGER,
            policy_state TEXT,
            policy_csl TEXT,
            policy_deductable INTEGER,
            policy_annual_premium REAL,
            umbrella_limit INTEGER,
            insured_sex TEXT,
            insured_education_level TEXT,
            insured_occupation TEXT,
            insured_hobbies TEXT,
            capital_gains INTEGER,
            capital_loss INTEGER
        )
    ''')
    # Table for blockchain data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blockchain (
            "index" INTEGER PRIMARY KEY,
            previous_hash TEXT,
            proof INTEGER,
            timestamp REAL,
            transactions TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Run the table creation function
if __name__ == '__main__':
    create_tables()
import sqlite3
import random

# Database file path
DATABASE = 'insurance_claims.db'

# Function to create tables
def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Table for claims data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            months_as_customer INTEGER,
            age INTEGER,
            policy_state TEXT,
            policy_csl TEXT,
            policy_deductable INTEGER,
            policy_annual_premium REAL,
            umbrella_limit INTEGER,
            insured_sex TEXT,
            insured_education_level TEXT,
            insured_occupation TEXT,
            insured_hobbies TEXT,
            capital_gains INTEGER,
            capital_loss INTEGER
        )
    ''')
    # Table for blockchain data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blockchain (
            "index" INTEGER PRIMARY KEY,
            previous_hash TEXT,
            proof INTEGER,
            timestamp REAL,
            transactions TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert sample records
def insert_sample_records():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    for _ in range(30):
        cursor.execute('''
            INSERT INTO claims (months_as_customer, age, policy_state, policy_csl, policy_deductable, 
                                policy_annual_premium, umbrella_limit, insured_sex, insured_education_level, 
                                insured_occupation, insured_hobbies, capital_gains, capital_loss)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            random.randint(1, 120),  # months_as_customer
            random.randint(18, 70),  # age
            random.choice(['CA', 'TX', 'NY', 'FL']),  # policy_state
            random.choice(['100/300', '250/500', '500/1000']),  # policy_csl
            random.randint(0, 2000),  # policy_deductable
            random.uniform(200.0, 1000.0),  # policy_annual_premium
            random.randint(0, 100000),  # umbrella_limit
            random.choice(['Male', 'Female']),  # insured_sex
            random.choice(['High School', 'Bachelors', 'Masters']),  # insured_education_level
            random.choice(['Engineer', 'Doctor', 'Teacher', 'Artist']),  # insured_occupation
            random.choice(['Reading', 'Traveling', 'Sports']),  # insured_hobbies
            random.randint(0, 10000),  # capital_gains
            random.randint(0, 10000)   # capital_loss
        ))
    
    conn.commit()
    conn.close()


def get_top_records():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM claims LIMIT 5')
    records = cursor.fetchall()
    conn.close()
    return records

# Function to insert sample records

# Run the table creation function and insert sample records
if __name__ == '__main__':
    create_tables()
    create_tables()
    insert_sample_records()
    get_top_records()
