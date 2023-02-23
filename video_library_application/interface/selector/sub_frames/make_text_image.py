from video_library_application.config.sizes.fixed_sizes import ImageSize
from video_library_application.config.colours import Colours
from video_library_application.config.font import Font
from PIL import Image, ImageFont, ImageDraw


class TextImage:
    """Contains methods to create tkinter images displaying text when given said text as an input"""

    fill_percent = 0.85  # fraction of image width text occupies
    font_name = Font.name + ".ttf"  # set font name
    text_colour = Colours.background  # set text colour

    @classmethod
    def make_text_image(cls, text):
        """Takes some text and the picture dimensions and returns an image"""
        def split_string(string_to_split):
            """Split string into two strings to place in image"""

            # split string into words
            list_string = string_to_split.split(" ")

            if len(list_string) == 1:  # if only one word return
                return list_string

            count_character = 0  # count number of characters into the string
            count_word = 0  # count number of word in the string

            for i in range(len(list_string)):  # loop over characters in string
                if count_character < (len(string_to_split)/2): # less than halfway through the string
                    count_character += len(list_string[i]) + 1 # set character to end of next word
                    count_word += 1  # add one to word count
                else:  # over half way
                    break
                if i + 1 == len(list_string):  # last loop
                    count_word -= 1 # go to previous word so short section is on top

            # set first return string
            string1 = list_string[0]
            for i in range(1,  count_word):
                string1 = string1 + " " + list_string[i]
            string2 = list_string[count_word]
            # set second return string
            for i in range(count_word + 1, len(list_string)):
                string2 = string2 + " " + list_string[i]
            return [string1, string2]

        # test size to use to find dimensions of text
        pt_size = 10
        #
        scale_factor = pt_size * ImageSize.width * cls.fill_percent
        # create blank image
        img = Image.new('RGB', (ImageSize.width, ImageSize.height), color=Colours.box)
        # test font size
        fnt = ImageFont.truetype(cls.font_name, pt_size)
        # set image to draw on
        d = ImageDraw.Draw(img)

        # split text into two strings in list
        strings = split_string(text)

        if len(strings) == 1:  # if one word
            font_size = fnt.getsize(strings[0]) # get test font size
            pt_size = int(scale_factor / font_size[0])
            fnt = ImageFont.truetype(cls.font_name, pt_size) # set new font size
            font_size = fnt.getsize(strings[0]) # get new font size to check it is not too high

            if font_size[1] > ImageSize.height * cls.fill_percent: # if too high
                scale_factor = pt_size * ImageSize.height * cls.fill_percent # set new scale factor
                fnt = ImageFont.truetype(cls.font_name, int(scale_factor / font_size[1])) # set new font size
                font_size = fnt.getsize(text) # size after height adjustment

            # draw text onto blank image
            d.text((((ImageSize.width - font_size[0]) / 2),
                    ((ImageSize.height - font_size[1]) / 2)), strings[0], font=fnt, fill=cls.text_colour)
        else:
            font_size1 = fnt.getsize(strings[0]) # test size of the two strings
            font_size2 = fnt.getsize(strings[1])

            if font_size1[0] > font_size2[0]: # if first word string is longer
                pt_size = int(scale_factor / font_size1[0])  # set font pt size
            else: # if second word string is longer
                pt_size = int(scale_factor / font_size2[0])  # set font pt size

            fnt = ImageFont.truetype(cls.font_name, pt_size)  # set font

            font_size1 = fnt.getsize(strings[0]) # size after width adjustment
            font_size2 = fnt.getsize(strings[1])

            if font_size1[1] + font_size2[1] > ImageSize.height * cls.fill_percent: # if too high
                scale_factor = pt_size * ImageSize.height * cls.fill_percent / 2 # set new scale factor
                if font_size1[1] > font_size2[1]:  # if first word is higher
                    pt_size = int(scale_factor / font_size1[1]) # set new pt font size
                else:
                    pt_size = int(scale_factor / font_size2[1])

                fnt = ImageFont.truetype(cls.font_name, pt_size) # set font

                font_size1 = fnt.getsize(strings[0]) # size after height adjustment
                font_size2 = fnt.getsize(strings[1])

            shift = 0.08 # set amount to adjust the text position so the string are positioned pleasingly
            # draw the two strings onto the blank image with the second string below the first
            d.text((((ImageSize.width - font_size1[0]) / 2), ((ImageSize.height / 2) - font_size1[1] * (shift + 1))), strings[0], font=fnt, fill=cls.text_colour)
            d.text((((ImageSize.width - font_size2[0]) / 2), (ImageSize.height / 2)+ font_size1[1] * shift), strings[1], font=fnt, fill=cls.text_colour)

        return img # created image
