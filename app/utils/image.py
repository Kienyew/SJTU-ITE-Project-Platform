from flask import current_app
from typing import List

import hashlib
import os
from ..project import forms
from PIL import Image

IMAGE_DESIRE_WIDTH = 1280  # Should probably put this inside a config file
IMAGE_DESIRE_HEIGHT = 1920


def compress_and_save(p_img: Image, save_path: str):
    """A helper function to compress a single image and save
    
    :param p_img: A pillow.Image object
    :param save_path: full save path in string
    :return: none (should probably return status)
    """
    
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


def save_image(img_container) -> str:
    """save data from FileStorage and return the name of compressed file
    
    :param img_container: werkzeug.datastructures.FileStorage
    :return: always return a filename(str) that reside in 'static > user resources > <filename>'
    """
    
    print(img_container)
    if img_container.filename:
        i = Image.open(img_container)
        # Hash file data from stream to avoid naming collision
        f_name, f_ext = os.path.splitext(img_container.filename)
        new_name = hashlib.sha256(i.tobytes()).hexdigest() + f_ext
        save_path = os.path.join(current_app.root_path, "static", "user resources", new_name)
        print(f'Original : {f_name} + {f_ext}\n New name : {new_name}\n Save path : {save_path}')  # DEBUG

        compress_and_save(i, save_path)
        return new_name
    return ''


def delete_image(image_name: str):
    """A helper function to compare newly added images to old one and delete
    
    :param image_name: image name of user project pic
    :return: none (should probably return boolean status)
    """
    if not image_name:
        return
    img_path = os.path.join(current_app.root_path, 'static', 'user resources', image_name)
    if os.path.isfile(img_path):
        print(f"Removing: {img_path}")
        os.remove(img_path)


def process_all_images(delete_toggle, old_pic, new_pic) -> [str]:
    for idx in range(4):  # delete unused image first
        if delete_toggle[idx] or new_pic[idx].filename:
            delete_image(old_pic[idx])
            if delete_toggle[idx]:
                old_pic[idx] = ''
            else:  # New image
                new_filename = save_image(new_pic[idx])
                old_pic[idx] = new_filename
    
    # Ensure the pic names are in sequence
    for i in range(3, -1, -1):
        if not old_pic[i]:
            old_pic.pop(i)
            old_pic.append('')
    
    return old_pic
