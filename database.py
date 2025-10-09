# Add database.py
import os
import psycopg2
import json
from datetime import datetime

class BankDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        self.create_tables()
    
    def create_tables(self):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash BYTEA,
                    salt BYTEA,
                    email TEXT,
                    account_balance REAL,
                    registration_date TEXT
                )
            ''')
        self.conn.commit()