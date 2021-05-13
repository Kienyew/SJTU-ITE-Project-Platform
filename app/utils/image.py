import hashlib, os
from ..project import forms
from PIL import Image
from run import app  # TODO: BETTER solution to get root path to avoid circular import

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


def save_images(form: forms.PublishProjectForm) -> [str]:
    filenames = []
    for data in [form.project_pic1.data, form.project_pic2.data, form.project_pic3.data, form.project_pic4.data]:
        if data:
            i = Image.open(data)
            # Hash file data from stream to avoid naming collision
            f_name, f_ext = os.path.splitext(data.filename)
            new_name = hashlib.sha256(i.tobytes()).hexdigest() + f_ext
            save_path = os.path.join(app.root_path, "static", "user resources", new_name)
            print(f'Original : {f_name} + {f_ext}\n New name : {new_name}\n Save path : {save_path}')  # DEBUG
            
            compress_and_save(i, save_path)
            filenames.append(new_name)
        else:
            filenames.append("")
    
    print("\n".join(filenames))
    return filenames
