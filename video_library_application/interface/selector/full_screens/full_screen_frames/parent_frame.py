from video_library_application.config.sizes.fixed_sizes import MainGridDimensions, MenuSize
from video_library_application.config.colours import Colours
from video_library_application.interface.selector.menu.menu_frames.menu_icon_frame import MenuIconFrame
from video_library_application.interface.selector.menu.menu_frames.menu_list_frame import MenuListFrame

import tkinter as tk


class ParentFrame(tk.Frame):
    """Constructs the tkinter parent frame which the other full-screen frames inherit from"""

    frame_size = MainGridDimensions  # set frame size

    def __init__(self, parent):
        """Constructs the parent frame, setting attributes, a matrix for the sub-frames and a menu object """
        tk.Frame.__init__(self, parent)
        self.config(bg=Colours.background)  # sets the background colour
        self.frames = [[] for _ in range(self.frame_size.row)]  # matrix for the frames
        self.focus_set()  # set so can get key-presses

        for i in range(self.frame_size.column):  # set the column width for each column
            self.columnconfigure(i, weight=1)

        self.menu_icon = MenuIconFrame(self)  # create menu icon that will display in top right corner

    def add_menu(self):
        """Adds a menu list to the current frame, and places in the correct position"""
        # get position of menu icon
        x_pos = self.menu_icon.winfo_rootx()
        y_pos = self.menu_icon.winfo_rooty()

        self.menu_list = MenuListFrame(self)  # create list of menu option
        self.menu_list.place(x=x_pos-MenuSize.width, y=y_pos)  # place in correct position
        self.menu_list.update()  # update so can find size

        self.menu_icon.highlight()  # highlight the icon

    def remove_menu(self):
        """Removes menu list from the current screen"""
        self.menu_list.place_forget()
        self.menu_list.destroy()
        self.menu_icon.lowlight()  # put the icon back to the normal colour