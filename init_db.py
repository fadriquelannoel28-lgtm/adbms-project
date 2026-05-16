#!/usr/bin/env python
"""
Database initialization script - Direct MySQL approach
"""

import pymysql
from config import Config

def init_db():
    """Initialize the database and create all tables"""
    
    # Connect to the database
    conn = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT,
    )
    
    cursor = conn.cursor()
    
    # Create User table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            middle_name VARCHAR(50),
            last_name VARCHAR(50) NOT NULL,
            gender VARCHAR(10) DEFAULT 'Unknown',
            phone VARCHAR(20) DEFAULT 'Not Set',
            email VARCHAR(100) UNIQUE NOT NULL,
            birthdate DATE,
            profile_pic VARCHAR(200) DEFAULT 'default-image.jpg',
            gov_id_pic VARCHAR(200),
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(30) DEFAULT 'staff',
            verify BOOLEAN DEFAULT FALSE,
            date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_username (username),
            INDEX idx_email (email)
        )
    ''')
    print("✓ Created user table")
    
    # Create MedInventory table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS med_inventory (
            id INT AUTO_INCREMENT PRIMARY KEY,
            img_med VARCHAR(200) DEFAULT 'images/thumbnail-med.jpg',
            medicine_name VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            dosage INT NOT NULL,
            quantity INT NOT NULL,
            per_price FLOAT NOT NULL,
            expiry_date DATE NOT NULL,
            user_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id),
            INDEX idx_medicine_name (medicine_name)
        )
    ''')
    print("✓ Created med_inventory table")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n✓ Database initialization complete!")
    print(f"✓ Database: {Config.DB_NAME}")
    print(f"✓ Tables created: user, med_inventory")

if __name__ == '__main__':
    init_db()
