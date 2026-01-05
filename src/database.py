import mysql.connector
from mysql.connector import Error
import sys

class Database:
    """Database connection manager with error handling"""
    
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                port=self.config.get('port', 3306),
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password']
            )
            
            if self.connection.is_connected():
                print("Successfully connected to database")
                
        except Error as e:
            print(f"ERROR: Failed to connect to database: {e}")
            print("Please check your database configuration and ensure MySQL is running")
            sys.exit(1)
    
    def get_connection(self):
        """Get database connection"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection
    
    def execute_query(self, query, params=None):
        """Execute a query (INSERT, UPDATE, DELETE)"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except Error as e:
            self.connection.rollback()
            raise Exception(f"Query execution failed: {e}")
    
    def execute_select(self, query, params=None):
        """Execute a SELECT query and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            raise Exception(f"Select query failed: {e}")
    
    def execute_transaction(self, queries):
        """Execute multiple queries in a transaction"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            self.connection.start_transaction()
            
            results = []
            for query, params in queries:
                cursor.execute(query, params or ())
                if query.strip().upper().startswith('INSERT'):
                    results.append(cursor.lastrowid)
                else:
                    results.append(cursor.rowcount)
            
            self.connection.commit()
            cursor.close()
            return results
            
        except Error as e:
            if self.connection:
                self.connection.rollback()
            if cursor:
                cursor.close()
            raise Exception(f"Transaction failed: {e}")
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
