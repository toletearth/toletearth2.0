"""
Creates database/properties.db and seeds it with sample listings.
Run once: python database/seed.py
Safe to re-run — it drops and recreates the table.
"""
import sqlite3
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "properties.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price INTEGER NOT NULL,
    city TEXT NOT NULL,
    sector TEXT NOT NULL,
    property_type TEXT NOT NULL,
    bhk INTEGER NOT NULL,
    sqft INTEGER NOT NULL,
    furnishing TEXT NOT NULL,
    tag TEXT,
    image TEXT NOT NULL,
    description TEXT,
    owner_name TEXT,
    owner_phone TEXT
);
"""

SAMPLE = [
    ("2 BHK Flat", 18000, "Mohali", "Sector 70", "Flat", 2, 1100, "Semi-Furnished", "Featured",
     "1.jpg", "Bright 2 BHK on a quiet street, close to markets and schools.", "Rajeev Sharma", "98140-00001"),
    ("3 BHK Builder Floor", 25000, "Chandigarh", "Sector 11", "Builder Floor", 3, 1500, "Furnished", "Featured",
     "2.jpg", "Independent floor with private terrace and covered parking.", "Anita Kapoor", "98140-00002"),
    ("2 BHK Flat", 16500, "Panchkula", "Sector 20", "Flat", 2, 1000, "Unfurnished", "New",
     "3.jpg", "Well-ventilated flat, second floor, lift access.", "Manpreet Singh", "98140-00003"),
    ("3 BHK Flat", 22000, "Mohali", "Aerocity", "Flat", 3, 1000, "Semi-Furnished", "New",
     "4.jpg", "Modern society flat with gym and park access.", "Neha Verma", "98140-00004"),
    ("1 BHK Flat", 11000, "Chandigarh", "Sector 22", "Flat", 1, 650, "Semi-Furnished", None,
     "5.jpg", "Compact and central, ideal for a single tenant or couple.", "Harpreet Kaur", "98140-00005"),
    ("2 BHK Independent House", 20000, "Panchkula", "Sector 8", "Independent House", 2, 1200, "Unfurnished", None,
     "6.jpg", "Ground floor of an independent house with a small yard.", "Sanjay Mehta", "98140-00006"),
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS properties;")
    cur.execute(SCHEMA)
    cur.executemany(
        """INSERT INTO properties
           (title, price, city, sector, property_type, bhk, sqft, furnishing, tag, image, description, owner_name, owner_phone)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        SAMPLE,
    )
    conn.commit()
    conn.close()
    print(f"Seeded {len(SAMPLE)} properties into {DB_PATH}")

if __name__ == "__main__":
    main()
