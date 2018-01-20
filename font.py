import sqlite3

from letter import Letter


class Font:
    FONT_1 = 1
    FONT_2 = 2
    FONT_3 = 3

    __letters = dict()

    def __init__(self, basic_font=None, letters=None):
        if basic_font is not None:
            self.__load_basic_font(basic_font)
        elif letters is not None:
            self.__letters = letters

    def __load_basic_font(self, basic_font):
        conn = sqlite3.connect('letters/base_fonts')
        c = conn.cursor()
        c.execute('SELECT letter_char , local_image , y_offset , x_offset , `width` '
                  'FROM  Letter '
                  'WHERE font_id = \'{}\''.format(basic_font))
        for letter in c.fetchall():
            self.__letters[letter[0]] = Letter(char=letter[0],
                                               image_path=letter[1],
                                               y_offset=letter[2],
                                               x_offset=letter[3],
                                               width=letter[4])

    def get_letter_image(self, char):
        return self.__letters[char].get_image()

    def get_letter_width(self, char):
        return self.__letters[char].get_width()

    def get_letter_x_offset(self, char):
        return self.__letters[char].get_x_offset()

    def get_letter_y_offset(self, char):
        return self.__letters[char].get_y_offset()

    def is_contains_letter(self, char):
        return char in self.__letters.keys()


if __name__ == '__main__':
    print(type(Font(basic_font=1).get_letter_width('x')))
