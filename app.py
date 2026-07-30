import os
import sqlite3

from flask import Flask, render_template, request, g

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "properties.db")

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    db = get_db()
    featured = db.execute(
        "SELECT * FROM properties WHERE tag IS NOT NULL ORDER BY id DESC LIMIT 4"
    ).fetchall()
    stats = {
        "listed": db.execute("SELECT COUNT(*) FROM properties").fetchone()[0],
        "users": 500,
        "saved": "12,50,000",
    }
    return render_template("index.html", featured=featured, stats=stats)


@app.route("/properties")
def properties():
    db = get_db()

    location = request.args.get("location", "").strip()
    property_type = request.args.get("property_type", "").strip()
    bhk = request.args.get("bhk", "").strip()
    budget = request.args.get("budget", "").strip()

    query = "SELECT * FROM properties WHERE 1=1"
    params = []

    if location:
        query += " AND (city LIKE ? OR sector LIKE ?)"
        params.extend([f"%{location}%", f"%{location}%"])
    if property_type:
        query += " AND property_type = ?"
        params.append(property_type)
    if bhk:
        query += " AND bhk = ?"
        params.append(bhk)
    if budget == "under-15000":
        query += " AND price < 15000"
    elif budget == "15000-25000":
        query += " AND price BETWEEN 15000 AND 25000"
    elif budget == "25000-plus":
        query += " AND price > 25000"

    query += " ORDER BY id DESC"
    listings = db.execute(query, params).fetchall()

    return render_template(
        "properties.html",
        listings=listings,
        filters={
            "location": location,
            "property_type": property_type,
            "bhk": bhk,
            "budget": budget,
        },
    )


@app.route("/property/<int:property_id>")
def property_details(property_id):
    db = get_db()
    listing = db.execute(
        "SELECT * FROM properties WHERE id = ?", (property_id,)
    ).fetchone()
    if listing is None:
        return render_template("property_details.html", listing=None), 404

    similar = db.execute(
        "SELECT * FROM properties WHERE city = ? AND id != ? LIMIT 3",
        (listing["city"], property_id),
    ).fetchall()
    return render_template("property_details.html", listing=listing, similar=similar)


@app.route("/list-property", methods=["GET", "POST"])
def list_property():
    submitted = False
    if request.method == "POST":
        # In production: validate input, save the listing (as unpublished/
        # pending review), and store any uploaded photos.
        submitted = True
    return render_template("list_property.html", submitted=submitted)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    submitted = False
    if request.method == "POST":
        # In production: validate input and persist / email the enquiry.
        submitted = True
    return render_template("contact.html", submitted=submitted)


@app.route("/faq")
def faq():
    return render_template("faq.html")


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        raise SystemExit(
            "database/properties.db not found — run `python database/seed.py` first."
        )
    app.run(debug=True)
