import os
import random
import shutil
import string

from PIL import Image, ImageDraw

from src.config import MEDIA_ROOT


# load_dotenv()


def save_img(folder, file):
    image_dir = os.path.join(MEDIA_ROOT, "media", "images", folder)
    # Create the upload directory if it doesn't exist
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    # get the destination path
    destination = os.path.join(image_dir, file.filename)
    return destination


def save_file(folder, file):
    # file_dir = os.path.join(MEDIA_ROOT, "media", "attachement", folder)
    file_dir = os.path.join(MEDIA_ROOT, folder)
    file_path = os.path.join(file_dir, file.filename)

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    if os.path.exists(file_path):
        base, extension = os.path.splitext(file_path)

        while os.path.exists(file_path):
            base = base + '_' + ''.join(random.choices(string.ascii_uppercase, k=5))
            file_path = f"{base}{extension}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    stored_path = os.path.join(folder, file.filename).replace("\\", "/")
    # destination = os.path.join(file_dir, file.filename)
    return stored_path


def create_and_save_image(folder, filename, width, height):
    file_dir = os.path.join(MEDIA_ROOT, "media", folder)

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    file_path = os.path.join(file_dir, filename)

    background_color = (255, 255, 255)  # RGB for white
    image = Image.new("RGB", (width, height), background_color)

    draw = ImageDraw.Draw(image)

    rectangle_color = (255, 0, 0)  # RGB for red
    rectangle_coordinates = [(50, 50), (250, 150)]
    draw.rectangle(rectangle_coordinates, fill=rectangle_color)

    # Save the image as a JPG file
    image.save(file_path, "JPEG")

    return file_path


def create_and_save_text_file(filename, content):
    file_dir = os.path.join(MEDIA_ROOT, "media", "txt_files")

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    file_path = os.path.join(file_dir, filename)

    # Write the content to the text file
    with open(file_path, "w") as file:
        file.write(content)

    return file_path
