from video_library_application.config.sizes.fixed_sizes import MenuSize
from video_library_application.config.sizes.relative_sizes import RelativeSizes
from video_library_application.config.colours import Colours
from video_library_application.config.font import Font
from video_library_application.directory_simulation.navigation import navigation
from video_library_application.interface.selector.menu.menu_position import MenuPosition
from video_library_application.interface.selector.menu.menu_frames.progress_bar_frame import ProgressBarFrame
import tkinter as tk


class MenuListFrame(tk.Frame):
    """Creates the menu list of options which appears in the full-screen home frame and the selection frames when the
    user has pressed the menu key"""

    # text to appear as the options in the menu
    button_text = ["Update (All)", "Update (Top Folders)", "Wipe Progress", "Exit"]

    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg=Colours.border)
        self.pack_propagate(0)

        # list to hold the buttons in the menu
        self.buttons = [self.make_button(self.button_text[0])]
        # add to frame
        self.buttons[0].pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # if at a selection frame with folders below it, add option to check the top folders to changes
        if navigation.is_only_files_below() is False and navigation.is_home() is False:
            self.buttons.append(self.make_button(self.button_text[1]))
            self.buttons[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=1)
        # if at a folder two or more levels down, offer option to wipe the progress at the location
        if navigation.get_level() >= 2:
            self.buttons.append(self.make_button(self.button_text[2]))
            self.buttons[-1].pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # add option to exit application
        self.buttons.append(self.make_button(self.button_text[3]))
        self.buttons[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=1)

        # set size of the limit frame
        self.config(bg=Colours.border, width=MenuSize.width, height=MenuSize.icon_size * len(self.buttons))
        # create object to deal with the position the user has selected or will select within the list
        self.buttons_matrix = self.frames_data = [[] for _ in range(len(self.buttons))]
        for i in range(len(self.buttons)):
            self.buttons_matrix[i].append(self.buttons[i])
        self.position = MenuPosition(self, self.buttons_matrix, Colours.border, Colours.box)

    def make_button(self, text):
        """returns a button when given some text to display in it"""
        return tk.Label(self, text=text, font=(Font.name, RelativeSizes.get_height_percent(3.5)),
                        bg=Colours.border,
                        fg=Colours.text)

    def make_progress_bar(self):
        """Add a progress bar to the bottom of the list to display when scanning for new video files"""
        self.config(height=MenuSize.icon_size * len(self.buttons) + MenuSize.progress_height)
        self.progress_bar = ProgressBarFrame(self)
        self.progress_bar.pack(side=tk.TOP)
        self.update()



