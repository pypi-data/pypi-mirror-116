
from typing import List
from io import BytesIO
import base64

from PIL import Image


def get_base64_images(image_paths: List[str], resize=None):
    b64_images = []
    for img_path in image_paths:
        with Image.open(img_path) as img:
            if resize is not None:
                img.thumbnail((resize, resize))
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            b64_images.append(
                base64.b64encode(buffered.getvalue()).decode('ascii')
            )
    return b64_images
