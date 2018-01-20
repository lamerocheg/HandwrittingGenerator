from PIL import Image


class Letter:
    __char = None
    __image = None
    __width = None
    __x_offset = None
    __y_offset = None

    def __init__(self, char, image_path, width, x_offset, y_offset):
        self.__char = char
        self.__image = Image.open(image_path, mode='r')
        self.__image.load()
        self.__width = width
        self.__x_offset = x_offset
        self.__y_offset = y_offset

    def get_char(self):
        return self.__char

    def get_image(self):
        return self.__image

    def get_width(self):
        return self.__width

    def get_x_offset(self):
        return self.__x_offset

    def get_y_offset(self):
        return self.__y_offset
