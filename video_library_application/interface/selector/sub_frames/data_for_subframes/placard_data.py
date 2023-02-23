from video_library_application.directory_simulation.navigation import navigation
from .blank_data import BlankData


class PlacardData(BlankData):
    """Contains data to make a image containing text to display the categories"""
    def __init__(self):
        super().__init__()
        self.name = navigation.current_folder.name
