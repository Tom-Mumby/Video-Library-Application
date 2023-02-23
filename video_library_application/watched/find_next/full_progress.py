from video_library_application.directory_simulation.navigation import navigation


class FullProgress:
    """Finds next video to watch if the video just watched was watched to the end"""

    def __init__(self):
        self.clear_data()

    def clear_data(self):
        """resets the class variables ready to run again"""
        self.from_top = None
        self.from_after = None
        self.just_watched_path = None
        self.reached_file = False

    def find(self, do_at_second_level=True):
        """finds the next video file that could be watched"""
        def check_file():
            """checks the current file to see if it the next one"""
            if self.reached_file:  # if gone past the just watched file in the directory structure
                if self.from_after is None:  # if not found suitable file after yet
                    if navigation.get_progress() != 1:  # if the file hasn't been watched
                        self.from_after = navigation.get_location()[2:]  # this file must be suitable to watch next so save location
            else:  # if not reached the just watched file yet
                if navigation.get_location() == self.just_watched_path:  # if at the just watched file
                    self.reached_file = True

                elif self.from_top is None:  # if not found suitable file before yet
                    if navigation.get_progress() != 1:  # if the file hasn't been watched
                        self.from_top = navigation.get_location()[2:]  # this file must be suitable to watch next so save location

        self.clear_data()  # reset variables
        self.just_watched_path = navigation.get_location()[:]  # get the current position

        if do_at_second_level:
            navigation.do_at_level(lambda: navigation.do_in_elements(check_file, include_files=True), level=2)
        else:  # do at current location
            navigation.do_in_elements(check_file, include_files=True)

        if self.from_after is not None:  # if next file to watch is after the current file
            return self.from_after
        elif self.from_top is not None:  # if next file is before the current file in the directory order
            return self.from_top
        else:
            return None  # all videos watched
