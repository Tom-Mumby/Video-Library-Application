from ...config.system_type import SystemType
from .video_controls import VideoControls

import vlc
import tkinter as tk


class PlayerFrame(tk.Frame):
    """Frame for the media player that inherits from the tkinter frame class, contains methods to alter playing state"""
    def __init__(self, parent):
        """Creates the frame and binds keypress event to function"""
        tk.Frame.__init__(self, parent)
        self.config(bg="black")

        self.source = ""

        # add arguments when creating vlc instance to remove error messages on Linux
        args = ["--verbose=-1"]
        if SystemType.isLinux:
            args.append('--no-xlib')

        # creates vlc instance
        self.vlc_instance = vlc.Instance(args)

        # creating a media player
        self.player = self.vlc_instance.media_player_new()
        self.player.audio_set_volume(100)

        # set player to tkinter frame
        if SystemType.isWindows:
            self.player.set_hwnd(self.winfo_id())
        self.player.set_xwindow(self.winfo_id())  # fails on Windows

        # create object to handle pausing / skipping through media
        self.video_controls = VideoControls(self.player)

    def change_media(self, source, start_position):
        """Changes playing video and sets it to a starting position"""

        # creates media from filepath
        media = self.vlc_instance.media_new(source)
        # sets media to player
        self.player.set_media(media)
        self.player.set_fullscreen(True)  # needed to stop stuttering on pi
        # play media
        self.player.play()

        # if selected jump to start position
        if start_position:
            self.player.set_position(start_position)

        # update playing variable
        self.video_controls.set_playing(True)