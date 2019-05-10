from flask import render_template,Blueprint
import os

style_transfer = Blueprint("style_transfer",__name__)


@style_transfer.route("/style_transfer")
def style_main_route():
    base_path = "application/static/style_images/"
    images = os.listdir(base_path)
    return render_template("style_transfer/style_transfer.html",images = images)
