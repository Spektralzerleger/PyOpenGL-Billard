"""
Last modified: 20.06.2020
here we load the textures ...
"""

from PIL import Image
from graphics import *


def check_file_existance(filename):
    try:
        with open(filename) as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False


def load_texture(filename):
    # check whether file exists
    if check_file_existance(filename) == False:
        print(filename + " not found")
        return 0

    # load image
    img = Image.open(filename)
    img_data = np.array(list(img.getdata()), np.uint8)
    width = img.size[0]
    height = img.size[1]

    # create texture
    ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, ID)
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data
    )

    # set texture filter
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return ID
