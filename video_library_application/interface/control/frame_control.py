
from ...directory_simulation.navigation import navigation
from video_library_application.interface.selector.full_screens.full_screen_frames.home_frame import HomeFrame
from video_library_application.interface.selector.full_screens.full_screen_frames.selection_frame import SelectionFrame


class FrameControl:
    """Controls the full-screen frames within the tkinter application, contains methods to: add, remove, and update frames"""

    def __init__(self, container):
        """Sets up the parent of the frames and instantiates the home frame"""

        # tkinter application frames are the children of
        self.container = container

        self.frames = []  # list to hold the tkinter frames
        self.frames.append(HomeFrame(self.container))  # add home selection frame
        self.frames[0].grid(row=0, column=0, sticky="nsew")

    def update_position(self, key_code):
        """Updates the position of the selected element within the frame"""
        self.frames[-1].position.change_position(key_code)

    def get_selected_child_name(self):
        """Returns the name of the element within the frame which is currently selected"""
        return self.frames[-1].get_selected()

    def get_last(self):
        """Returns the last selection frame"""
        return self.frames[-1]

    def update_frames_above(self):
        """Updates all frames above the current one"""

        # if current folder length greater than
        current_folder = navigation.get_location()[:]
        level = len(current_folder)

        if level > 1: # not at home
            navigation.go_back_home()
            navigation.go_to_folder(current_folder[0])

            for i in range(1, level):
                self.frames[i].update_frames()
                navigation.go_to_folder(current_folder[i])

    def update_all_frames(self):
        """Updates current frame after the user has finished watching the video file"""
        self.update_frames_above()

        if len(self.frames) > 1:
            self.frames[-1].update_frames()
            self.frames[-1].tkraise()  # raise the last frame
            self.frames[-1].focus_set()
        self.frames[0].update_watched(True)

    def update_watched_frames(self):
        """Update the watched list in the home frame"""
        if len(self.frames) != 1:
            self.frames[0].update_watched()

    def make_selection_frame(self, select_name=None):
        """Makes a new selection frame based on the navigation object location"""
        self.frames.append(SelectionFrame(self.container, select_name))
        self.frames[-1].grid(row=0, column=0, sticky="nsew")

    def delete_last_frame(self):
        """Removes the last frame in the list of frame; used when user presses back"""
        self.frames[-1].grid_forget()
        self.frames[-1].destroy()
        del self.frames[-1]

    def go_back_frame(self):
        """Removes last frame and goes back to previous"""
        if len(self.frames) != 1:  # if not at home
            navigation.go_back()
            self.delete_last_frame()
            self.frames[-1].tkraise()
            self.frames[-1].focus_set()

    def go_back_to_home(self):
        """Goes back to the home frame and deletes all others"""
        num_frames = len(self.frames)
        if num_frames == 1:
            self.frames[0].position.reset_after_watched()
        else:
            for i in range(num_frames):
                self.go_back_frame()

    def reload_frame(self):
        """Reloads last frame in list"""
        self.update_frames_above()
        self.update_watched_frames()

        if len(self.frames) == 1:  # if at home
            self.frames.append(HomeFrame(self.container))
        else:
            self.frames.append(SelectionFrame(self.container))
        # grid frame
        self.frames[-1].grid(row=0, column=0, sticky="nsew")
        # put frame on top
        self.frames[-1].tkraise()
        # delete old frame
        self.frames[-2].grid_forget()
        self.frames[-2].destroy()
        del self.frames[-2]