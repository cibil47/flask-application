from flask import current_app
from application.models import User

import secrets, os
from PIL import Image

def save_file(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_filename)
    output_size = (125, 125)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)
    resized_image.save(picture_path)
    # form_picture.save(picture_path)
    return picture_filename



def check_username(uname):

    db_user = User.query.filter_by(username=uname).first()
    if db_user:
        return "true"
    return "false"


def check_email(email):

    db_user = User.query.filter_by(email=email).first()
    if db_user:
        return "true"
    return "false"