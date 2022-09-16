import os
# pip install pillow
from PIL import Image
import random
from flask import current_app
from io import BytesIO


def add_pic(pic_content, pic_name, title):

    filename = pic_name
    # Grab extension type .jpg or .png
    ext_type = filename.split('.')[-1]
    storage_filename = str(title) + str(random.randint(0, 100)) + '.' + ext_type

    filepath = os.path.join(current_app.root_path, 'static/post_photos', storage_filename)
    # Open the picture and save it
    pic = Image.open(BytesIO(pic_content))
    # pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename
