from video_library_application.directory_simulation.navigation import navigation


class NoProgress: # state of current video file
    """Finds next video to watch if the video just watched was reset to the start"""

    def __init__(self):
        self.clear_data()

    def clear_data(self):
        """resets the class variables ready to run again"""
        self.next_file = None
        self.full_progress = True  # as top counts as well
        self.has_a_fully_watched = False

    def find(self):
        """finds the next video file that could be watched"""
        def check_file():
            """checks the current file to see if it the next one"""
            progress = navigation.get_progress()

            if progress != 1:
                if self.full_progress is True:
                    self.next_file = navigation.get_location()[2:]

            if progress == 1:
                self.full_progress = True
            else:
                self.full_progress = False

        def find_partially_watched():
            """set next file if current video is partially watched"""
            progress = navigation.get_progress()
            if progress is not None and progress != 1:
                self.next_file = navigation.get_location()[2:]

        def contains_a_fully_watched():
            """check if current video has been fully watched"""
            if navigation.get_progress() == 1:
                if self.has_a_fully_watched is False:
                    self.has_a_fully_watched = True
        self.clear_data()  # reset variables
        navigation.do_at_level(lambda: navigation.do_in_elements(contains_a_fully_watched, include_files=True), level=2)
        if self.has_a_fully_watched:
            navigation.do_at_level(lambda: navigation.do_in_elements(check_file, include_files=True), level=2)
            # return false if all fully watched
        else:
            navigation.do_at_level(lambda: navigation.do_in_elements(find_partially_watched, include_files=True), level=2)
            # return false if all empty
        return self.next_file