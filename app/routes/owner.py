from flask import Blueprint, render_template, request

owner_bp = Blueprint("owner", __name__)


@owner_bp.route("/list-property", methods=["GET", "POST"])
def list_property():
    submitted = False
    if request.method == "POST":
        # In production: validate input, save the listing (as unpublished /
        # pending review) via a properties-service write function, and
        # store any uploaded photos into property_images.
        submitted = True
    return render_template("list_property.html", submitted=submitted)
