from flask import current_app
from typing import List

import hashlib
import os
from ..project import forms
from PIL import Image

IMAGE_DESIRE_WIDTH = 1280  # Should probably put this inside a config file
IMAGE_DESIRE_HEIGHT = 1920


def compress_and_save(p_img: Image, save_path: str):
    if p_img.size[0] > IMAGE_DESIRE_WIDTH:
        w_percent = IMAGE_DESIRE_WIDTH / float(p_img.size[0])
        h_size = int(float(p_img.size[1]) * float(w_percent))
        p_img = p_img.resize((IMAGE_DESIRE_WIDTH, h_size), Image.LANCZOS)
    elif p_img.size[1] > IMAGE_DESIRE_HEIGHT:
        h_percent = IMAGE_DESIRE_HEIGHT / float(p_img.size[1])
        w_size = int(float(p_img.size[0]) * float(h_percent))
        p_img = p_img.resize((w_size, IMAGE_DESIRE_HEIGHT), Image.LANCZOS)
    p_img.save(save_path, optimize=True, quality=85)
    # TODO: Add raise if error


def save_images(form: forms.PublishProjectForm) -> List[str]:
    """
    Wouldn't create new data if previous data exist, otherwise compress and save
    
    :param form:
    :return: always return a List[str] with four picture names inside  'static > user resources > <filename>'
    """
    
    filenames = []
    for data in [form.project_pic1.data, form.project_pic2.data, form.project_pic3.data, form.project_pic4.data]:
        if data:
            if os.path.isfile(os.path.join(current_app.root_path, "static", "user resources", data.filename)):
                filenames.append(data.filename)
                continue
                
            i = Image.open(data)
            # Hash file data from stream to avoid naming collision
            f_name, f_ext = os.path.splitext(data.filename)
            new_name = hashlib.sha256(i.tobytes()).hexdigest() + f_ext
            save_path = os.path.join(current_app.root_path, "static", "user resources", new_name)
            # DEBUG
            print(f'Original : {f_name} + {f_ext}\n New name : {new_name}\n Save path : {save_path}')

            compress_and_save(i, save_path)
            filenames.append(new_name)
            # Ensure the picture is always store in sequential

    print("\n".join(filenames))
    filenames = filenames + ['' for _ in range(len(filenames), 4)]  # Ensure the return length is always 4
    return filenames


def delete_unused_image(form: forms.PublishProjectForm, old_images: [str]):
    for new_image in [form.project_pic1.data, form.project_pic2.data, form.project_pic3.data, form.project_pic4.data]:
        if new_image and new_image.filename in old_images:
            old_images.remove(new_image.filename)
            
    for image in old_images:
        if image:
            print(f"Removing: {os.path.join(current_app.root_path, 'static', 'user resources', image)}")
            os.remove(os.path.join(current_app.root_path, "static", "user resources", image))
