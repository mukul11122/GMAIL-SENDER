import sqlite3
import os
from datetime import datetime
from config import DATABASE_SETTINGS

class Database:
    def __init__(self):
        self.db_path = DATABASE_SETTINGS['db_path']
        self._create_tables()
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def _create_tables(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                store_code TEXT,
                mobile_number TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                gmail_account TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gmail_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                emails_sent_today INTEGER DEFAULT 0,
                last_reset_date DATE DEFAULT CURRENT_DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raw_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_customer(self, email, store_code=None, mobile_number=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO customers (email, store_code, mobile_number) VALUES (?, ?, ?)',
                (email, store_code, mobile_number)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def add_customers_batch(self, customers):
        conn = self._get_connection()
        cursor = conn.cursor()
        added = 0
        for customer in customers:
            try:
                cursor.execute(
                    'INSERT INTO customers (email, store_code, mobile_number) VALUES (?, ?, ?)',
                    (customer.get('email'), customer.get('store_code'), customer.get('mobile_number'))
                )
                added += 1
            except sqlite3.IntegrityError:
                pass
        conn.commit()
        conn.close()
        return added
    
    def get_customers(self, limit=None, offset=0):
        conn = self._get_connection()
        cursor = conn.cursor()
        if limit:
            cursor.execute('SELECT * FROM customers LIMIT ? OFFSET ?', (limit, offset))
        else:
            cursor.execute('SELECT * FROM customers')
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_unsent_customers(self, limit=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        if limit:
            cursor.execute('''
                SELECT * FROM customers 
                WHERE id NOT IN (SELECT customer_id FROM email_logs WHERE status = 'sent')
                LIMIT ?
            ''', (limit,))
        else:
            cursor.execute('''
                SELECT * FROM customers 
                WHERE id NOT IN (SELECT customer_id FROM email_logs WHERE status = 'sent')
            ''')
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_customers_by_ids(self, ids):
        if not ids:
            return []
        conn = self._get_connection()
        cursor = conn.cursor()
        placeholders = ','.join('?' * len(ids))
        cursor.execute(f'''
            SELECT * FROM customers 
            WHERE id NOT IN (SELECT customer_id FROM email_logs WHERE status = 'sent')
            AND id IN ({placeholders})
        ''', ids)
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_failed_emails_count(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT customer_id, COUNT(*) as fail_count 
            FROM email_logs 
            WHERE status = 'failed'
            GROUP BY customer_id
        ''')
        failed = cursor.fetchall()
        conn.close()
        return {row[0]: row[1] for row in failed}
    
    def get_invalid_emails(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT c.email FROM customers c
            WHERE c.email NOT LIKE '%@%.%'
            OR c.email LIKE '%@%'
            OR substr(c.email, 1, 1) = '@'
            OR c.email NOT GLOB '*[a-zA-Z0-9]*'
        ''')
        emails = [row[0] for row in cursor.fetchall()]
        conn.close()
        return emails
    
    def get_customers_with_failures(self, min_failures=2):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.id, c.email, c.store_code, c.mobile_number, COUNT(el.id) as fail_count
            FROM customers c
            JOIN email_logs el ON c.id = el.customer_id AND el.status = 'failed'
            GROUP BY c.id
            HAVING COUNT(el.id) >= ?
        ''', (min_failures,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_unsent_customers(self, limit=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        if limit:
            cursor.execute('''
                SELECT * FROM customers 
                WHERE id NOT IN (SELECT customer_id FROM email_logs WHERE status = 'sent')
                LIMIT ?
            ''', (limit,))
        else:
            cursor.execute('''
                SELECT * FROM customers 
                WHERE id NOT IN (SELECT customer_id FROM email_logs WHERE status = 'sent')
            ''')
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_unsent_customers_by_ids(self, ids):
        if not ids:
            return []
        conn = self._get_connection()
        cursor = conn.cursor()
        placeholders = ','.join('?' * len(ids))
        cursor.execute(f'''
            SELECT * FROM customers 
            WHERE id NOT IN (SELECT customer_id FROM email_logs WHERE status = 'sent')
            AND id IN ({placeholders})
        ''', ids)
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_customers_by_ids(self, ids):
        if not ids:
            return []
        conn = self._get_connection()
        cursor = conn.cursor()
        placeholders = ','.join('?' * len(ids))
        cursor.execute(f'''
            SELECT * FROM customers 
            WHERE id NOT IN (SELECT customer_id FROM email_logs WHERE status = 'sent')
            AND id IN ({placeholders})
        ''', ids)
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def delete_customers_by_email(self, emails):
        conn = self._get_connection()
        cursor = conn.cursor()
        placeholders = ','.join('?' * len(emails))
        cursor.execute(f'DELETE FROM email_logs WHERE customer_id IN (SELECT id FROM customers WHERE email IN ({placeholders}))', emails)
        cursor.execute(f'DELETE FROM customers WHERE email IN ({placeholders})', emails)
        conn.commit()
        conn.close()
    
    def get_unsent_customers_by_ids(self, ids):
        if not ids:
            return []
        conn = self._get_connection()
        cursor = conn.cursor()
        placeholders = ','.join('?' * len(ids))
        cursor.execute(f'''
            SELECT * FROM customers 
            WHERE id NOT IN (SELECT customer_id FROM email_logs WHERE status = 'sent')
            AND id IN ({placeholders})
        ''', ids)
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_customer_count(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM customers')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_unsent_count(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM customers 
            WHERE id NOT IN (SELECT customer_id FROM email_logs WHERE status = 'sent')
        ''')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def log_email(self, customer_id, gmail_account, status):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO email_logs (customer_id, gmail_account, status) VALUES (?, ?, ?)',
            (customer_id, gmail_account, status)
        )
        conn.commit()
        conn.close()
    
    def add_gmail_account(self, email, password):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO gmail_accounts (email, password) VALUES (?, ?)',
                (email, password)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_gmail_accounts(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, is_active, emails_sent_today, last_reset_date FROM gmail_accounts WHERE is_active = 1')
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_daily_sent_count(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        today = datetime.now().date().isoformat()
        cursor.execute('''
            SELECT SUM(emails_sent_today) FROM gmail_accounts 
            WHERE last_reset_date = ?
        ''', (today,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result[0] else 0
    
    def get_available_gmail_account(self):
        from config import EMAIL_SETTINGS
        conn = self._get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().date().isoformat()
        
        cursor.execute('''
            UPDATE gmail_accounts 
            SET emails_sent_today = 0, last_reset_date = ?
            WHERE last_reset_date < ?
        ''', (today, today))
        conn.commit()
        
        cursor.execute('''
            SELECT id, email, password FROM gmail_accounts 
            WHERE is_active = 1 AND emails_sent_today < ?
            ORDER BY emails_sent_today ASC
            LIMIT 1
        ''', (EMAIL_SETTINGS['max_emails_per_account_per_day'],))
        
        row = cursor.fetchone()
        conn.close()
        return row
    
    def increment_email_count(self, account_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE gmail_accounts SET emails_sent_today = emails_sent_today + 1 WHERE id = ?',
            (account_id,)
        )
        conn.commit()
        conn.close()
    
    def delete_gmail_account(self, email):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM gmail_accounts WHERE email = ?', (email,))
        conn.commit()
        conn.close()
    
    def add_stock_data(self, raw_data):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO stock_data (raw_data) VALUES (?)',
            (raw_data,)
        )
        conn.commit()
        conn.close()
    
    def get_latest_stock_data(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT raw_data FROM stock_data ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]
    
    def clear_stock_data(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM stock_data')
        conn.commit()
        conn.close()
    
    def clear_customers(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM customers')
        cursor.execute('DELETE FROM email_logs')
        conn.commit()
        conn.close()
    
    def reset_email_logs(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM email_logs')
        conn.commit()
        conn.close()

if __name__ == '__main__':
    db = Database()
    print("Database initialized successfully!")
