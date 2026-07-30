"""
Every read used by the routes/templates goes through here, so there is one
place that knows the schema. Routes and templates never write raw SQL.

Rows are returned as plain dicts with template-friendly aliases:
  - area_sqft -> sqft
  - rent      -> price
  - featured  -> tag ("Featured" or None)
so the existing templates keep working unchanged against the new schema.
"""
from app.models.db import get_db

BASE_SELECT = """
SELECT
    p.id, p.title, p.description, p.property_type, p.bhk,
    p.bathrooms, p.balconies, p.area_sqft AS sqft,
    p.rent AS price, p.security_deposit,
    c.name AS city, s.name AS sector,
    p.address, p.latitude, p.longitude,
    p.furnishing, p.parking, p.lift, p.power_backup, p.wifi,
    p.pet_friendly, p.bachelor_allowed, p.family_allowed,
    p.verified, p.featured, p.status,
    u.name AS owner_name, u.phone AS owner_phone, u.email AS owner_email,
    (SELECT image_path FROM property_images pi
       WHERE pi.property_id = p.id
       ORDER BY pi.display_order LIMIT 1) AS image
FROM properties p
JOIN cities c ON c.id = p.city_id
JOIN sectors s ON s.id = p.sector_id
JOIN users u ON u.id = p.owner_id
"""


def _with_tag(row):
    d = dict(row)
    d["tag"] = "Featured" if d.get("featured") else None
    return d


def get_stats():
    db = get_db()
    listed = db.execute(
        "SELECT COUNT(*) FROM properties WHERE status = 'available'"
    ).fetchone()[0]
    return {"listed": listed, "users": 500, "saved": "12,50,000"}


def get_featured_properties(limit=4):
    db = get_db()
    rows = db.execute(
        BASE_SELECT + " WHERE p.status = 'available' AND p.featured = 1 "
        "ORDER BY p.id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [_with_tag(r) for r in rows]


def search_properties(filters):
    db = get_db()
    query = BASE_SELECT + " WHERE p.status = 'available'"
    params = []

    location = filters.get("location")
    if location:
        query += " AND (c.name LIKE ? OR s.name LIKE ?)"
        params.extend([f"%{location}%", f"%{location}%"])

    property_type = filters.get("property_type")
    if property_type:
        query += " AND p.property_type = ?"
        params.append(property_type)

    bhk = filters.get("bhk")
    if bhk:
        query += " AND p.bhk = ?"
        params.append(bhk)

    budget = filters.get("budget")
    if budget == "under-15000":
        query += " AND p.rent < 15000"
    elif budget == "15000-25000":
        query += " AND p.rent BETWEEN 15000 AND 25000"
    elif budget == "25000-plus":
        query += " AND p.rent > 25000"

    query += " ORDER BY p.id DESC"
    rows = db.execute(query, params).fetchall()
    return [_with_tag(r) for r in rows]


def get_property(property_id):
    db = get_db()
    row = db.execute(BASE_SELECT + " WHERE p.id = ?", (property_id,)).fetchone()
    return _with_tag(row) if row else None


def get_similar_properties(city_name, exclude_id, limit=3):
    db = get_db()
    rows = db.execute(
        BASE_SELECT + " WHERE c.name = ? AND p.id != ? AND p.status = 'available' "
        "LIMIT ?",
        (city_name, exclude_id, limit),
    ).fetchall()
    return [_with_tag(r) for r in rows]
