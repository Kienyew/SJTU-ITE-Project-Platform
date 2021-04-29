import io

from PIL import Image


def compress(image_data: bytes) -> bytes:
    output = io.BytesIO()
    image = Image.open(io.BytesIO(image_data))
    image.save(output, image.format)
    return output.getvalue()
