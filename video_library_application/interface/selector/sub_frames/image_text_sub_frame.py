from video_library_application.config.sizes.fixed_sizes import ImageSize
from video_library_application.config.colours import Colours
from video_library_application.config.font import Font
from video_library_application.config.sizes.relative_sizes import RelativeSizes
from .image_sub_frame import SubFrameImage

import tkinter as tk
import tkinter.font as tkf


class SubFrameImageText(SubFrameImage):
    """tkinter frame which displays an image and text, contains methods to set text and update"""

    def __init__(self, parent, frame_data, shrink=False):
        """Create image and text within the frame"""
        super().__init__(parent, frame_data)
        if shrink is True:
            self.text_scale = 1.1
            self.text_lines = 3
        else:
            self.text_scale = 1.3
            self.text_lines = 2

        adjust_name = self.check_text_size()
        # make text label
        self.label_information = tk.Label(self, text=adjust_name, height=self.text_lines, wraplength=ImageSize.width, font=(
            Font.name, RelativeSizes.get_text_size(self.text_scale)), bg=Colours.background, fg=Colours.text)
        self.label_information.pack()

    def update_text(self, frame_data):
        """Updates the text"""
        self.update_image(frame_data)  # updates image
        adjust_name = self.check_text_size()

        self.label_information.configure(text=adjust_name)  # updates text

    def check_text_size(self):
        """Checks if text is too large, returning smaller size if it is. Problem with long words, can solve by splitting up into words but can take some time to run"""
        font = tkf.Font(size=RelativeSizes.get_text_size(self.text_scale), family=Font.name)
        full_length = font.measure(self.frame_data.name)

        text_ratio = (ImageSize.width * self.text_lines) / full_length

        if text_ratio > 1:
            return self.frame_data.name

        cut_char = int(text_ratio * len(self.frame_data.name) * 0.7)

        return self.frame_data.name[:cut_char] + "..."