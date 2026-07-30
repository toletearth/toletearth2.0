from flask import Blueprint, render_template, request

from app.services.property_service import get_featured_properties, get_stats

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template(
        "index.html",
        featured=get_featured_properties(4),
        stats=get_stats(),
    )


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    submitted = False
    if request.method == "POST":
        # In production: validate input and persist / email the enquiry.
        submitted = True
    return render_template("contact.html", submitted=submitted)


@main_bp.route("/faq")
def faq():
    return render_template("faq.html")
