from flask import Blueprint, render_template, request

from app.services.property_service import (
    get_property,
    get_similar_properties,
    search_properties,
)

properties_bp = Blueprint("properties", __name__)


@properties_bp.route("/properties")
def browse():
    filters = {
        "location": request.args.get("location", "").strip(),
        "property_type": request.args.get("property_type", "").strip(),
        "bhk": request.args.get("bhk", "").strip(),
        "budget": request.args.get("budget", "").strip(),
    }
    listings = search_properties(filters)
    return render_template("properties.html", listings=listings, filters=filters)


@properties_bp.route("/property/<int:property_id>")
def details(property_id):
    listing = get_property(property_id)
    if listing is None:
        return render_template("property_details.html", listing=None), 404

    similar = get_similar_properties(listing["city"], property_id, limit=3)
    return render_template("property_details.html", listing=listing, similar=similar)
