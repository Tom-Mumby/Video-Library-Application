from video_library_application.config.key_press import KeyPress
from video_library_application.prepare.prerequisite_files_check import PrerequisiteFilesCheck  # needed so prepare runs before watched list
from video_library_application.directory_simulation.navigation import navigation
from video_library_application.watched import manage_watched
from video_library_application.interface.player.player_frame import PlayerFrame
from .control.frame_control import FrameControl
from .control.menu_control import MenuControl

import threading
import tkinter as tk


class SelectorApplication(tk.Tk):
    """Creates the main tkinter application and deals with any keypress from the user"""
    def __init__(self):
        """Sets a container to hold the full-screen home and selection frames, also sets up the media_player frame and
        object to control which full-screen frame is displayed and the menu feature"""
        tk.Tk.__init__(self)
        self.attributes('-fullscreen', True)  # set to ful screen
        self.config(cursor="none")  # stop cursor displaying

        self.container = tk.Frame(self)  # contains the stacked frames
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.video_player = PlayerFrame(self.container)  # creates media player frame
        self.video_player.grid(row=0, column=0, sticky="nsew")

        self.frames = FrameControl(self.container)
        self.menu = MenuControl(self.frames)

        self.bind("<Key>", self.handle_keypress)  # bind method that handles when a key is pressed

    def handle_keypress(self, event):
        """Handles the keypress, creating new frames or deleting and going back to old frames"""

        def handle_if_playing():

            playing = self.video_player.video_controls.keypress(key_code)  # true, false or none
            if playing is None:
                # if video has just stopped playing
                manage_watched.manage.finished_watching(self.video_player.video_controls.get_position())
                self.frames.update_all_frames()
                if key_code == KeyPress.back:
                    return True  # to avoid going back again
                else:  # home pressed
                    return False  # carry on with method
            else:
                return playing

        def make_next_frame():
            """Creates the next frame, can be another selection frame or can set the video file to play"""

            def launch_player():
                """Starts video playing from navigation object location"""
                manage_watched.manage.before_watching()
                self.video_player.change_media(navigation.get_full_path(), navigation.get_progress())
                self.video_player.tkraise()
                self.video_player.focus_set()
                if type(child_name) is list:  # if video file was selected from the recently watched in the home screen
                    # creates new thread to make the extra frames
                    threading.Thread(target=make_watched_frames, daemon=True).start()  # possibly a bit much!

            def make_watched_frames():
                """If a watched item on the home screen is pressed, make the selection frame that would be needed in order to reach it"""

                def make_frame(child_name, select_name=None):
                    navigation.go_to_folder(child_name)
                    self.frames.make_selection_frame(select_name) #chage from select frame
                    self.video_player.tkraise()

                is_single_file = navigation.is_file_in_single_folder()
                level = len(child_name)

                navigation.go_back(level)  # go back to home
                self.video_player.tkraise()

                for k in range(level-2):  # go into each folder and make new frame
                    make_frame(child_name[k], child_name[k+1])

                if is_single_file:  # should work for this
                    navigation.go_to_folder(child_name[-2])
                else:

                    make_frame(child_name[level-2], child_name[level-1])

                navigation.go_to_folder(child_name[-1])

                self.update()  # force tkinter to update frames
                self.video_player.focus_set()

            child_name = self.frames.get_selected_child_name()  # get folder to go into, can be list
            navigation.go_to_folder(child_name)
            if navigation.is_folder() is False: # video file selected
                launch_player()  # start playing video
            elif navigation.is_single_file_under():
                navigation.go_to_folder_index(0)  # go into file
                launch_player()

            else: # if in folder
                self.frames.make_selection_frame()

        key_code = event.keysym  # get key code

        if handle_if_playing():  # deal with if playing, if is playing return so the next part is not used
            return

        if self.menu.is_showing():  # if the menu is showing in front of the frame
            # pass the keycode to the object to handle
            if self.menu.keypress_menu(key_code):  # if has done update
                self.frames.reload_frame()
            return

        # enter
        elif key_code == KeyPress.enter:
            make_next_frame()  # deals with creating the correct next frame
        # back
        elif key_code == KeyPress.back:
            self.frames.go_back_frame()  # goes back and deletes he last frame
        # home
        elif key_code == KeyPress.home:
            self.frames.go_back_to_home()  # goes back to home deleting all of the frames
        elif key_code == KeyPress.menu_or_subtitles:  # if menu button is pressed
            self.menu.add_menu(self.frames.get_last())  # create menu object in current frame
        else:
            self.frames.update_position(key_code)  # if none of these must be update the position of the current frame
