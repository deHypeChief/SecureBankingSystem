# Add database.py
import os
import psycopg2
import json
from datetime import datetime

class BankDatabase:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            print("✅ Database connected successfully!")
            self.create_tables()
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    def create_tables(self):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash BYTEA,
                    salt BYTEA,
                    email TEXT,
                    account_balance REAL DEFAULT 0.0,
                    registration_date TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    username TEXT REFERENCES users(username),
                    created_at TEXT,
                    expires_at TEXT
                )
            ''')
        self.conn.commit()
    
    def insert_user(self, username, password_hash, salt, email, account_balance=0.0):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO users (username, password_hash, salt, email, account_balance, registration_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (username, password_hash, salt, email, account_balance, datetime.now().isoformat()))
        self.conn.commit()
    
    def get_user_by_username(self, username):
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            return cursor.fetchone()
    
    def insert_session(self, session_id, username, expires_at):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO sessions (session_id, username, created_at, expires_at)
                VALUES (%s, %s, %s, %s)
            ''', (session_id, username, datetime.now().isoformat(), expires_at.isoformat()))
        self.conn.commit()
    
    def get_session(self, session_id):
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM sessions WHERE session_id = %s', (session_id,))
            return cursor.fetchone()
    
    def delete_session(self, session_id):
        with self.conn.cursor() as cursor:
            cursor.execute('DELETE FROM sessions WHERE session_id = %s', (session_id,))
        self.conn.commit()