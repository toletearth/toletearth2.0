"""
Creates instance/toletearth.db from migrations/001_initial_schema.sql and
loads starter data — replacing both the old database/properties.db and the
hardcoded PROPERTIES list that used to live in app.py.

Run once, from the project root:
    python migrations/seed_db.py

Safe to re-run: it deletes and rebuilds the database file each time.
"""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(BASE_DIR, "migrations", "001_initial_schema.sql")
DB_PATH = os.path.join(BASE_DIR, "instance", "toletearth.db")

CITIES = ["Chandigarh", "Mohali", "Panchkula"]

SECTORS = {
    "Chandigarh": ["Sector 11", "Sector 22", "Sector 35-A"],
    "Mohali": ["Sector 70", "Aerocity"],
    "Panchkula": ["Sector 20", "Sector 8"],
}

OWNERS = [
    ("Rajeev Sharma", "9814000001", "rajeev@example.com"),
    ("Anita Kapoor", "9814000002", "anita@example.com"),
    ("Manpreet Singh", "9814000003", "manpreet@example.com"),
    ("Neha Verma", "9814000004", "neha@example.com"),
    ("Harpreet Kaur", "9814000005", "harpreet@example.com"),
    ("Sanjay Mehta", "9814000006", "sanjay@example.com"),
]

# (title, description, property_type, bhk, bathrooms, area_sqft, rent,
#  city, sector, furnishing, owner_index, featured, verified, image_file)
PROPERTIES = [
    ("2 BHK Flat", "Bright 2 BHK on a quiet street, close to markets and schools.",
     "Flat", 2, 2, 1100, 18000, "Mohali", "Sector 70", "Semi-Furnished", 0, 1, 1, "1.jpg"),
    ("3 BHK Builder Floor", "Independent floor with private terrace and covered parking.",
     "Builder Floor", 3, 2, 1500, 25000, "Chandigarh", "Sector 11", "Furnished", 1, 1, 1, "2.jpg"),
    ("2 BHK Flat", "Well-ventilated flat, second floor, lift access.",
     "Flat", 2, 2, 1000, 16500, "Panchkula", "Sector 20", "Unfurnished", 2, 1, 0, "3.jpg"),
    ("3 BHK Flat", "Modern society flat with gym and park access.",
     "Flat", 3, 2, 1000, 22000, "Mohali", "Aerocity", "Semi-Furnished", 3, 1, 1, "4.jpg"),
    ("1 BHK Flat", "Compact and central, ideal for a single tenant or couple.",
     "Flat", 1, 1, 650, 11000, "Chandigarh", "Sector 22", "Semi-Furnished", 4, 0, 0, "5.jpg"),
    ("2 BHK Independent House", "Ground floor of an independent house with a small yard.",
     "Independent House", 2, 1, 1200, 20000, "Panchkula", "Sector 8", "Unfurnished", 5, 0, 1, "6.jpg"),
]


def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())

    city_ids = {}
    for name in CITIES:
        cur = conn.execute("INSERT INTO cities (name) VALUES (?)", (name,))
        city_ids[name] = cur.lastrowid

    sector_ids = {}
    for city, sectors in SECTORS.items():
        for sector in sectors:
            cur = conn.execute(
                "INSERT INTO sectors (city_id, name) VALUES (?, ?)",
                (city_ids[city], sector),
            )
            sector_ids[(city, sector)] = cur.lastrowid

    owner_ids = []
    for name, phone, email in OWNERS:
        cur = conn.execute(
            "INSERT INTO users (name, phone, email, role) VALUES (?, ?, ?, 'owner')",
            (name, phone, email),
        )
        owner_ids.append(cur.lastrowid)

    for (title, desc, ptype, bhk, baths, sqft, rent, city, sector,
         furnishing, owner_idx, featured, verified, image_file) in PROPERTIES:
        cur = conn.execute(
            """INSERT INTO properties
               (title, description, property_type, bhk, bathrooms, area_sqft, rent,
                city_id, sector_id, furnishing, owner_id, featured, verified, status,
                parking, lift, wifi)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'available', 1, 0, 1)""",
            (title, desc, ptype, bhk, baths, sqft, rent,
             city_ids[city], sector_ids[(city, sector)], furnishing,
             owner_ids[owner_idx], featured, verified),
        )
        property_id = cur.lastrowid
        conn.execute(
            "INSERT INTO property_images (property_id, image_path, display_order) VALUES (?, ?, 0)",
            (property_id, f"properties/{image_file}"),
        )

    conn.commit()
    conn.close()
    print(f"Database created at {DB_PATH} with {len(PROPERTIES)} properties.")


if __name__ == "__main__":
    main()
