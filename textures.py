"""
Last modified: 28.06.2020

Texture help function, to load and work with textures efficiently.
"""

from PIL import Image
from graphics import *


def check_file_existance(filename):
    """Help function to check whether a file exists.

    Args:
        filename (string): Path to the file, e.g. "Textures/1.bmp"

    Returns:
        bool: True, if file exists. False, if not.
    """
    try:
        with open(filename) as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False


def load_texture(filename):
    """Function that reads an image file and saves a texture.

    Args:
        filename (string): Path to the file, e.g. "Textures/1.bmp"

    Returns:
        int: Texture ID. 0, if no file was found.
    """
    # Check whether file exists
    if check_file_existance(filename) == False:
        print(filename + " not found")
        return 0

    """glTexImage2D expects the first element of the image data to be the bottom-left corner of
    the image. Subsequent elements go left to right, with subsequent lines going from bottom to top.
    However, our read-in image data goes left to right and top to bottom.
    So, we need to flip the vertical coordinate y."""
    # Load image
    img = Image.open(filename).transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(list(img.getdata()), np.uint8)
    width = img.size[0]
    height = img.size[1]

    # Create texture
    ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, ID)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    # Set texture filter
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return ID
