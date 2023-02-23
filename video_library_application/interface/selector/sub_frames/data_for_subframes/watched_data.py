from .thumbnail_data import ThumbnailData
from video_library_application.directory_simulation.navigation import navigation


class WatchedData(ThumbnailData):
    """Contains data to make a thumbnail and label frame for a watched subframe, which will be displayed in the home frame"""
    def __init__(self):
        super().__init__()
        # sets name to contain all of the path infomation so can identify video file
        if navigation.is_file_in_single_folder():
            self.name = navigation.get_path(" - ", 0, 1)
        else:
            self.name = navigation.get_path(" - ", 1, 1) + " - " + self.name