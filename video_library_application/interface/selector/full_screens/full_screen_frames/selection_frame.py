from video_library_application.config.colours import Colours
from video_library_application.config.font import Font
from video_library_application.config.sizes.relative_sizes import RelativeSizes
from video_library_application.directory_simulation.navigation import navigation
from video_library_application.interface.selector.full_screens.full_screen_frames.parent_frame import ParentFrame
from video_library_application.interface.selector.full_screens.arrows.selection_arrows import ArrowUpDown
from video_library_application.interface.selector.full_screens.position.selection_position import GridPosition
from video_library_application.interface.selector.sub_frames.data_for_subframes.blank_data import BlankData  # this one is extra
from video_library_application.interface.selector.sub_frames.data_for_subframes.thumbnail_data import ThumbnailData
from video_library_application.interface.selector.sub_frames.image_text_sub_frame import SubFrameImageText

import tkinter as tk


class SelectionFrame(ParentFrame):
    """Constructs the selection frame, with the up/down scroll feature"""
    def __init__(self, parent, select_frame=None):
        """Adds the grid of frames and the down arrow if needed"""
        super().__init__(parent)

        self.number_children = navigation.get_num_children()  # gets the number of sub frames to make
        self.frames_data_rows = self.get_frame_data_rows()
        self.frames_data = [[] for _ in range(self.frames_data_rows)]  # matrix to hold the frames data

        self.load_frames()
        self.arrows = ArrowUpDown(self)

        for i in range(self.frame_size.row + 1):  # set the row widths
            self.rowconfigure(i, weight=1)
        # make the name of the directory label
        lb_directory = tk.Label(self, text=navigation.get_path(" - "), font=(Font.name, RelativeSizes.get_height_percent(6)), bg=Colours.background, fg=Colours.text)
        lb_directory.grid(row=0, column=0, sticky=tk.W, padx=RelativeSizes.get_height_percent(4), pady=RelativeSizes.get_height_percent(1), columnspan=3)

        self.menu_icon.grid(row=0, column=2, sticky=tk.E, padx=RelativeSizes.get_height_percent(4))  # adds menu icon

        self.arrows.arrow1.grid(row=1, column=0, columnspan=self.frame_size.column)

        for j in range(self.frame_size.row):  # loop over the frames on the screen
            for i in range(self.frame_size.column):
                self.frames[j].append(SubFrameImageText(self, self.frames_data[j][i]))  # create frames from frame data
                self.frames[j][i].grid(row=2 + j, column=i, sticky=tk.N)

        self.position = GridPosition(self.frames, self.frames_data, self.arrows, Colours.background, Colours.border)

        self.arrows.arrow2.grid(row=4, column=0, columnspan=self.frame_size.column, pady=RelativeSizes.get_height_percent(1.5))
        self.select_frame_boarder(select_frame)

    def get_frame_data_rows(self):
        """returns the number of rows needed to contain all of the sub-frames"""
        num_rows = int(self.number_children/self.frame_size.column)  # total number of rows
        if self.number_children % self.frame_size.column != 0:  # add an extra row if there are frames left over
            num_rows += 1

        if num_rows < self.frame_size.row:  # if there are fewer frames then rows on the screen
            return self.frame_size.row  # set the number of rows to the number of rows on the screen
        else:
            return num_rows

    def loop_over_frames(self, function, add_blank=False):
        """Moves the current location of the navigation object to the location of the folder/video in each sub-frame
        and calls a function to run there"""

        for j in range(self.frames_data_rows):  # loop over each frames
            for i in range(self.frame_size.column):
                if (i + j * self.frame_size.column) < self.number_children:  # it not go to then end of the frame data
                    navigation.go_to_folder_index(i+j*self.frame_size.column)  # go into folder
                    function(i, j)
                    navigation.go_back()
                else:  # if gone past the end of the frame data add a blank frame
                    if add_blank == True:
                        self.frames_data[j].append(BlankData())

    def load_frames(self):
        """Load the sub-frames into the full-screen frames"""
        def add_frame(i, j):
            self.frames_data[j].append(ThumbnailData())  # add frame data to array

        self.loop_over_frames(add_frame, add_blank=True)

    def update_frames(self):
        """Update the sub-frames, used when any changes have been made to them"""
        for i in range(self.frames_data_rows):
            self.frames_data[i].clear()
        self.load_frames()
        self.position.update_frames()

    def select_frame_boarder(self, frame_name_to_select=None):
        """Moves the selection boarder to a given frame"""
        def check_name(i, j):
            if frame_name_to_select is not None:
                if frame_name_to_select == navigation.get_current_name():  # check if frame name matches

                    self.position.select_frame(i,j)  # jump to desired frame

        self.loop_over_frames(check_name)

    def get_selected(self):
        """Get the name of the selected item"""
        index = self.position.get_location_index()
        return navigation.current_folder.children[index].name