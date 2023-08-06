import io

from PIL.Image import Image


def get_aspect_ratio(image: Image) -> float:
    """
    Aspect ratio of the image

    :param image: image to check
    :return: width/height
    """
    return (1.0*image.width)/image.height

def get_image(content: bytes = None, filepath: str = None) -> Image:
    """
    Get  the image

    :param content: bytes representing the image. Mututally exclusive with filepath
    :param filepath: filepath where the image is located. Mutually exclusive with content
    :return: image in memory
    """
    assert content or filepath, "Either content of filepath needs to be set"
    if filepath is not None:
        with open(filepath, mode="rb") as f:
            content = f.read()

    im = Image.open(io.BytesIO(content))
    return im


def is_valid_image(image: Image) -> bool:
    """
    Check if the image the user has passed in indeed a valid image or something totally
    different

    :param image: image to check
    :return: true if this is an image, false otherwise
    """
    try:
        image.verify()
    except Exception:
        return False
    else:
        return True


def scale_image(image: Image, new_width: int, new_height: int, keep_aspect_ratio: bool = True) -> Image:
    """
    Scale an image

    :param image: image to rescale
    :param new_width: the new width the image will have
    :param new_height: the new height the image will have
    :param keep_aspect_ratio: if set, we will try to preserve the aspect ratio (width/height) of the image. If set,
        the return value will not have the exact new_width/new_height yuo have input.
    :return a **copy** of the given image
    """
    if keep_aspect_ratio:
        return image.thumbnail(size=(new_width, new_height))
    else:
        return image.resize((new_width, new_height))
