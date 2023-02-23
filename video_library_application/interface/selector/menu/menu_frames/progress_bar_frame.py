import tkinter as tk
from video_library_application.config.sizes.fixed_sizes import MenuSize
from video_library_application.config.colours import Colours
from video_library_application.interface.selector.canvas_polygon import CanvasPolygon
import os


class ProgressBarFrame(tk.Frame):
    """Creates a frame to show the progress when scanning for new video files, appears at the bottom of the menu list"""

    # set size
    width = MenuSize.width
    height = MenuSize.progress_height
    # number of jumps the progress bar makes going from empty to full
    number_intervals = 10

    def __init__(self, parent):
        """Creates frame and adds a coloured canvas to it which will move across indicate progress through the search"""
        tk.Frame.__init__(self, parent)
        self.config(bg=Colours.border)
        # creates the progress indicator
        self.progress_coloured = CanvasPolygon(parent=self, x_size=self.width, y_size=self.height, colour=Colours.border)
        self.progress_coloured.add_to_frame()
        # sets the progress bar to it's initial position with no progress
        self.__update_bar(0)

        # holds the total number of folders directly under the current location
        self.total_folder_num = 0
        # holds the current number of folders directly under the current location which have been scanned
        self.current_folder_num = 0
        # holds the number of folders needed for the progress bar to make to the next stage
        self.multiple = 0

    def get_total_folder_number(self, folder_list):
        """returns the total number of folders directly under the current location"""

        for folder in folder_list:
            try:
                self.total_folder_num += len(os.listdir(folder))
            except FileNotFoundError:
                print("Folder not found, check if it has been deleted and scan from directory above")
                print(folder)
                exit()

        self.multiple = self.total_folder_num // self.number_intervals
        if self.multiple == 0:
            self.multiple = 1

    def update_progress(self):
        """Updates the position of the progress bar based on the number of folders scanned out of the total number"""
        if self.total_folder_num == 0:
            self.__update_bar(1)
            return

        self.current_folder_num += 1

        if self.total_folder_num == self.current_folder_num:
            self.__update_bar(1)

        elif self.current_folder_num % self.multiple == 0:
            self.__update_bar(self.current_folder_num / self.total_folder_num)

    def __update_bar(self, progress):
        """Updates progress bar when given a fraction of the total width to cover"""
        def get_box_points():
            return [0,0,  0,self.height, round(self.width*progress),self.height, round(self.width*progress),0]

        self.progress_coloured.remove_polygons()
        self.progress_coloured.add_polygon(get_box_points(), Colours.progress)
        self.update()




