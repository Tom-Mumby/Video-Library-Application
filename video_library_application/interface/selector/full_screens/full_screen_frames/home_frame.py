from video_library_application.config.colours import Colours
from video_library_application.config.font import Font
from video_library_application.config.sizes.relative_sizes import RelativeSizes
from video_library_application.directory_simulation.navigation import navigation
from video_library_application.watched import manage_watched

from video_library_application.interface.selector.full_screens.full_screen_frames.parent_frame import ParentFrame
from video_library_application.interface.selector.full_screens.arrows.home_arrows import ArrowAcross
from video_library_application.interface.selector.full_screens.position.home_position import SlidePosition
from video_library_application.interface.selector.sub_frames.data_for_subframes.placard_data import PlacardData
from video_library_application.interface.selector.sub_frames.data_for_subframes.blank_data import BlankData
from video_library_application.interface.selector.sub_frames.data_for_subframes.watched_data import WatchedData
from video_library_application.interface.selector.sub_frames.image_sub_frame import SubFrameImage
from video_library_application.interface.selector.sub_frames.image_text_sub_frame import SubFrameImageText

import tkinter as tk


class HomeFrame(ParentFrame):
    """Constructs the home frame, with the sliding top and bottom selector features"""
    def __init__(self, parent):
        """Adds the top and bottoms rows of frames and the arrows"""
        super().__init__(parent)

        self.frames_data = [[] for _ in range(self.frame_size.row)]  # matrix for the frame data
        self.watched_paths = []

        self.load_categories()
        self.load_watched()

        # set the row widths
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=3)

        # set the column widths
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=6)
        self.columnconfigure(2, weight=6)
        self.columnconfigure(3, weight=6)
        self.columnconfigure(4, weight=1)

        # create category label
        label_categories = tk.Label(self, text="Categories", font=(Font.name, RelativeSizes.get_height_percent(5)), bg=Colours.background, fg=Colours.text)
        label_categories.grid(row=0, column=0, sticky=tk.NW, padx=RelativeSizes.get_height_percent(4), pady=RelativeSizes.get_height_percent(4), columnspan=4)
        self.menu_icon.grid(row=0, column=3, sticky=tk.E)  # adds menu icon

        # create top arrows
        self.arrows_top = ArrowAcross(self)
        self.arrows_top.arrow1.grid(row=1, column=0, padx=RelativeSizes.get_height_percent(2))

        for i in range(self.frame_size.column):    # loops over number of columns
            self.frames[0].append(SubFrameImage(self, self.frames_data[0][i]))  # create category frames from frame data
            self.frames[0][i].grid(row=1, column=i+1, sticky=tk.N)

        self.arrows_top.arrow2.grid(row=1, column=4, padx=RelativeSizes.get_height_percent(2))

        # create watched label
        label_watched = tk.Label(self, text="Watch Next", font=(Font.name, RelativeSizes.get_height_percent(5)), bg=Colours.background, fg=Colours.text)
        label_watched.grid(row=2, column=0, sticky=tk.NW, padx=RelativeSizes.get_height_percent(4), pady=RelativeSizes.get_height_percent(2), columnspan=5)

        # create bottom arrows
        self.arrows_bottom = ArrowAcross(self)
        # add bottom arrows to grid
        self.arrows_bottom.arrow1.grid(row=3, column=0, sticky=tk.N, pady=RelativeSizes.get_height_percent(2), padx=RelativeSizes.get_height_percent(2))

        # create selection position object
        self.position = SlidePosition(self.frames, self.frames_data, self.arrows_top, self.arrows_bottom, Colours.background, Colours.border)  # create position object

        for i in range(self.frame_size.column):  # loops over number of columns
            self.frames[1].append(SubFrameImageText(self, self.frames_data[1][i], shrink=True))  # create watched frames from frame data
            self.frames[1][i].grid(row=3, column=i+1, sticky=tk.N)

        self.arrows_bottom.arrow2.grid(row=3, column=4, sticky=tk.N, pady=RelativeSizes.get_height_percent(2), padx=RelativeSizes.get_height_percent(2))

    def load_categories(self):
        """Add the video type categories to the top selection row"""
        number_categories = navigation.get_num_children()  # gets the number of video categories

        for i in range(number_categories):  # loop over the categories
            navigation.go_to_folder_index(i)  # go into each category folder
            self.frames_data[0].append(PlacardData())  # add the frame data
            navigation.go_back()

        for i in range(number_categories, self.frame_size.column):  # if any blank frames are needed
            self.frames_data[0].append(BlankData())  # add blank frame

    def load_watched(self):
        """Add the watched videos to the bottom selection row"""
        self.watched_paths = manage_watched.manage.get_home_paths()
        for i in range(len(self.watched_paths)):  # loop over the watched paths
            navigation.go_to_folder(self.watched_paths[i])  # go into each watched video file
            self.frames_data[1].append(WatchedData())  # add the frame data
            navigation.go_back(len(self.watched_paths[i]))

        for i in range(len(self.watched_paths), self.frame_size.column):  # if any blank frames are needed add blank frames
            self.frames_data[1].append(BlankData())

    def update_watched(self, reset_border=True):
        """Update the watched videos in the bottom row"""
        self.frames_data[1].clear()
        navigation.do_at_level(self.load_watched, 0)
        self.position.reset_after_watched(reset_border)  # doing too much

    def get_selected(self):
        """Returns the selected frame name"""
        index = self.position.get_location_index()
        if index[0] == 0:  # top row
            return navigation.current_folder.children[index[1]].name
        if index[0] == 1:  # bottom row
            return self.watched_paths[index[1]]