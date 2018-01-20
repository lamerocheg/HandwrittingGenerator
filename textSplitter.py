import re

from font import Font
from page import Page, A4

VOWELS_REGEXP = re.compile('[ёуеыаоэяию]')
SPACE_WIDTH = 15


class TextSplitter:

    def __get_word_length(self, word):

        ''' inner function for calculate length of provided word
        :param word: word for calculation. it can be single word or any part of text
        :return: sum of width for each symbols. if symbol not in current Font.keys() used SPACE_WIDTH value
        '''

        return sum([self.widths.get_letter_width(letter) + self.letter_spacing
                    if self.widths.is_contains_letter(letter)
                    else SPACE_WIDTH + self.letter_spacing for letter in word])

    def __split_word(self, word, remaining_width):
        ''' inner function for separate provided word into 2 part for the end of the line.

        for each vowels  except first and last 2 letters check whether left part of the word is suitable by length
        if left part of word is suitable - separate word into 2 part left_part + '-' and right_part for wrapping

        :param word:  word for splitting
        :param remaining_width: remaining width of current page row
        :return: tuple of left and right part of the word. Left part can be empty string
        '''
        vowels_positions = [i.start() + 2 for i in re.finditer(VOWELS_REGEXP, word.lower()[2:-2])]
        while len(vowels_positions) > 0:
            curr_vowels = vowels_positions.pop()
            right_part = word[curr_vowels + 1:]
            left_part = word[:curr_vowels + 1]
            if self.__get_word_length(left_part + '-') <= remaining_width:
                return left_part + '-', right_part
        return '', word

    def __append_single_line_to_page(self, line):

        '''inner function for append completed line to the page.
         check whether current page has space for line and append line into page or append page to pages list
         and create new page with current line only.

        :param line: line for appending
        '''

        if line[1] == True:
            line.append(self.__get_word_length(line[0]))

        if len(self.current_page) < self.row_count:
            self.current_page.append(line)
        else:
            self.pages.append(self.current_page)
            self.current_page = list([line])

    def __append_lines(self, text_line, align_center):
        '''inner function for append line from text into pages.
        it may take a some page lines or actually some pages.
        Also , centered lines doesn't separate word for text wrapping

        lines in pages array has format [text , align_center] where align center is flag for center-aligned text

        :param text_line: text for append into pages
        :param align_center: check whether this text has center align
        '''
        curr_page_line = ''
        curr_page_line_width = 0
        for word in re.split('\s', '  ' + text_line):
            word_length = self.__get_word_length(word)
            if curr_page_line_width + word_length <= self.page_width:
                curr_page_line += word + ' '
                curr_page_line_width += word_length + SPACE_WIDTH
            elif align_center:
                self.__append_single_line_to_page([curr_page_line, align_center])
                curr_page_line = word + ' '
                curr_page_line_width = self.__get_word_length(curr_page_line)
            else:
                left_part, right_part = self.__split_word(word, self.page_width - curr_page_line_width)
                self.__append_single_line_to_page([curr_page_line + left_part, align_center])
                curr_page_line = right_part + ' '
                curr_page_line_width = self.__get_word_length(curr_page_line)
        if len(curr_page_line) > 0:
            self.__append_single_line_to_page([curr_page_line, align_center])

    def __append_empty_lines(self, empty_line_count):
        ''' inner function for append empty lines to page.
        they should be a placed as single block since empty lines requires for images or tables

        :param empty_line_count: count of empty lines for append
        :return: current not-complete page
        '''
        if len(self.current_page) + empty_line_count <= self.row_count:
            self.current_page.extend([['', False]] * empty_line_count)
        elif empty_line_count < self.row_count:
            self.pages.append(self.current_page)
            self.current_page = [['', False]] * empty_line_count
        else:
            self.pages.append(self.current_page)
            self.pages.append([['', False]])
            self.current_page = list()

    def _split_text(self, text):
        ''' function for split text into lines and add each line to pages list

        :param text: text for formatting

        '''
        empty_line_count = 0
        for line in text.split('\n'):
            if len(line.strip()) == 0:
                empty_line_count += 1
                continue
            elif empty_line_count > 0:
                self.__append_empty_lines(empty_line_count)
                empty_line_count = 0
            align_center = line.startswith('  ')
            self.__append_lines(line, align_center)

            if self.requested_page and self.requested_page <= len(self.pages):
                break
        if len(self.current_page) > 0:
            self.pages.append(self.current_page)

    def __init__(self, text, font, page_format, is_compact=True, letter_spacing=0, requested_page=None):
        '''constructor for TextFormatter. initialize fields and call _split_text() function

        :param text: text for formatting
        :param font: current font
        :param page_format: current format of page , available choices A4 , A5_COMMON , A5_RING
        :param is_compact: flag for compact state, used cor calculate row_count for current format
        :param requested_page: if single page requested, only formatting will stop on requested page
        '''
        self.pages = list()
        self.widths = font
        self.format = page_format
        self.row_count = self.format.compact_row_count if is_compact else self.format.not_compact_row_count
        self.page_width = page_format.width - page_format.padding_left - page_format.padding_right
        self.requested_page = requested_page
        self.current_page = list()
        self.letter_spacing = letter_spacing
        self._split_text(text)

    def get_page(self, index):
        if index >= 1 and index <= len(self.pages):
            return self.pages[index - 1]
        else:
            return None

    def get_pages_count(self):
        return len(self.pages)

    def get_all_pages(self):
        return self.pages


# DO NOT REMOVE . it's requires for further debugging
if __name__ == '__main__':
    temp = '''Олег говорит, в Большой Быховщине три улицы: Гагарина, Первомайская и третья, название которой он все время забывает. 
Когда-то дискотекой гремел клуб, каждое утро открывалась школа, был фельдшерско-акушерский пункт. Когда-то — это давно. Теперь все закрыто.
Олег тоже не работает. Предыдущий наниматель не отдает $400, а устроиться больше некуда: несезон. Денег почти нет, надо платить алименты. Хорошо, что есть мама. У нее работа и хозяйство. В общем, история не для тех, кто получает за 500. Все равно не поймут. Да и не факт, что надо.
«Жесткая была тетка»
Жизнь вне дедлайнов, SMS-оповещений, лент Facebook, попыток объехать вечернюю пробку, карьерного роста, амбиций и планирования. Это необязательно «реальная Беларусь», это просто «в том числе Беларусь».
Низкая деревня захватывает домами пригорок. Олег, ежась, подходит на безлюдную остановку. Рядом магазин, когда-то работавший клуб и контора — в прошлом центр деревенской жизни.
В бывшем здании школы какой-то мужик поставил фермы, стал выращивать вешенки. История интересная. Он у банка взял четыре тысячи. Вроде небольшая сумма. Но потом мифическим образом пропал. В банке расстроились. Ищут человека. А дядька приезжий, из Санкт-Петербурга вроде. Просто корни отсюда.
До петербургского дядьки с вешенками здесь был центр колхоза. До колхоза — имение Радзивиллов.
«Раньше хоть клуб работал»
Сам Олег не очень старый, ему 33 года. Волосы с проседью, мешковатая черная куртка и почти постоянно зажатая между пальцев зажигалка. От старой жизни у него пятый iPhone да банковская карточка с вейпом, которыми он уже полгода не пользуется.

 Ноябрь прожил на 100 рублей. Я человек курящий. На сигареты ушло, не знаю, рублей 30. Интернет — 15. 55 рублей — чай, кофе, домой купить что-то. Машину я свою продал за тысячу долларов мужику из Могилева. Был Ford Mondeo. Продал, потому что в нее тоже надо вкладывать. А вкладывать нечего.
Еще полгода назад работал в Москве. Пришлось вернуться. Побыл один день в Минске на съемной квартире в Каменной Горке, а потом отдал хозяину ключи. Оказался в родной деревне.
Живу в режиме самосохранения»
Когда вернулся, подрядился заниматься ремонтом. Первое время все было прекрасно. Не московские заработки, но деньги. Потом пересеклись с конторой, которой требовалось доделать несколько домиков.
Вроде все было нормально. А как деньги отдавать, так человек посадил нас на завтраки. До сих пор ничего не отдал. Хотя оказалось, я сам дурак: подписал документы без указанного номера страхового свидетельства. Пустые, по сути. Предъявить ничего не могу — только давить на совесть. А с ней у человека как-то не очень. И что мне тут делать? Трактористом? Я не умею. Куда там еще? Водителем? Стаж нужен. А стройка — она как наркотик, к ней обязательно возвращаешься.
Мы ходим по всем трем улицам Большой Быховщины и не понимаем друг друга. Когда звучит вопрос, можно ли использовать слово «выживает» относительно его ситуации, Олег начинает крутиться.
 Блин, ну… Если по-честному, нет. Я не считаю, что я выживаю. Я живу в режиме самосохранения. То есть нет лишних трат. После Москвы потребности упали, пусть я человек совсем непритязательный. Драйва не хватает, но это терпимо. У меня теперь все просто: надо обеспечить свои биологические потребности и не сдохнуть до следующего появления денег… Хотя да, выживаю, получается…
«По одному ко мне»
У Олега почти боевая биография: училище в Клецке, служба в дикой 120-й дивизии (дикой, потому что хорошо воевала), еще одна служба, только уже по контракту, чистка кадров в части, слесарничество на заводе, а потом кино.
 Брат в этой теме крутится. Предложил мне быть рабочим. Потом стал плейбэкером. Показывал режиссеру отснятый материал. Жизнь наладилась. Стал водителем — самая блатная работа в кино. Водитель вечно всем недоволен и вечно получает больше всех. Самая маленькая моя выручка — $1100, самая большая — $2300. Возил осветителей, немножко им помогал, за это мне доплачивали. $2000 спокойно имел.
За забором зачем-то напрягается петух. Очень выделяется на фоне расслабленной атмосферы. Олег вспоминает одну из первых картин, на которых работал. «Слон» с Сергеем Шнуровым.
    '''
    print('\n\n')
    for line in TextSplitter(temp, Font(basic_font=1), Page(base_page_type=A4)).get_all_pages():
        print('\n\n\n\n\n')
        for l in line:
            print(l[0])
