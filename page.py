A4 = {'width': 1190,
      'height': 1684,
      'padding_top': 126,
      'compact_row_count': 52,
      'not_compact_row_count': 26,
      'padding_left': 170,
      'padding_right': 56}

A5_RING = {'width': 840,
           'height': 1190,
           'padding_top': 44,
           'compact_row_count': 39,
           'not_compact_row_count': 20,
           'padding_left': 86,
           'padding_right': 86}


class Page:

    def __init__(self, width=0, height=0, padding_top=0, compact_row_count=0,
                 not_compact_row_count=0, padding_left=0, padding_right=0, base_page_type=None):
        if base_page_type is not None:
            self.__init__(**base_page_type)
        else:
            self.width = width
            self.height = height
            self.padding_top = padding_top
            self.compact_row_count = compact_row_count
            self.not_compact_row_count = not_compact_row_count
            self.padding_left = padding_left
            self.padding_right = padding_right
