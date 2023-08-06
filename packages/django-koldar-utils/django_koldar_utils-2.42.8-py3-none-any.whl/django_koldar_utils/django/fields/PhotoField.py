import io
import math
import os
import uuid
from typing import Tuple, List, Dict, Optional

from PIL.Image import Image
from datasize import DataSize
from django.core.exceptions import ValidationError
from django.db import models

from django_koldar_utils.django.AbstractDjangoField import AbstractDjangoField
from django_koldar_utils.django.validators import validators
from django_koldar_utils.functions import image_helpers, math_helpers


class ScaledPictureField(models.ImageField):
    """
    A picture that is automatically resized to a maximum value
    if the user sends a bigger picture. The behavior is independent on validators
    """

    description = "Represents a photo the user uploads"

    def __init__(self, *args, min_width: int = 32, min_height: int = 32, max_width: int = 256, max_height: int = 256, **kwargs):
        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height

        super().__init__(*args, **kwargs)

    def deconstruct(self) -> Tuple[str, str, List[any], Dict[str, any]]:
        name, path, args, kwargs = super().deconstruct()
        kwargs["min_width"] = self.min_width
        kwargs["min_height"] = self.min_height
        kwargs["max_width"] = self.max_width
        kwargs["max_height"] = self.max_height

        return name, path, args, kwargs

    def pre_save(self, model_instance, add: bool) -> Image:
        image = image_helpers.get_image(filepath=model_instance.photo)

        w = math_helpers.bound(image.width, self.min_width, self.max_width)
        h = math_helpers.bound(image.height, self.min_height, self.max_height)

        if w != image.width or h != image.height:
            image = image_helpers.scale_image(image, w, h)

        setattr(model_instance, self.attname, image)
        return image

    def to_python(self, image) -> Optional[Image]:
        if image is None:
            return None

        if isinstance(image, bytes):
            im = Image.open(io.BytesIO(image))
        elif isinstance(image, str):
            im = Image.open(image.encode("utf8"))
        elif isinstance(image, Image):
            pass
        else:
            raise TypeError(f"Cannot handle type {type(image)}!")

        return im

        # try:
        #     limit = DataSize(self.picture_threshold)
        #     num_of_tries = 10
        #     img = Image.open(image.file)
        #     width, height = img.size
        #     ratio = float(width) / float(height)
        #
        #     if settings.FILE_UPLOAD_TEMP_DIR is not None:
        #         upload_dir = settings.FILE_UPLOAD_TEMP_DIR
        #     else:
        #         upload_dir = "/tmp"
        #
        #     tmp_file = open(os.path.join(upload_dir, str(uuid.uuid1())), "w")
        #     tmp_file.write(image.file.read())
        #     tmp_file.close()
        #
        #     while os.path.getsize(tmp_file.name) > limit:
        #         num_of_tries -= 1
        #         width = 900 if num_of_tries == 0 else width - 100
        #         height = int(width / ratio)
        #         img.thumbnail((width, height), Image.ANTIALIAS)
        #         img.save(tmp_file.name, img.format)
        #         image.file = open(tmp_file.name)
        #         if num_of_tries == 0:
        #             break
        # except:
        #     pass
        # return image


