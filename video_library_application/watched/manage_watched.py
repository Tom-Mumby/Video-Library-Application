from video_library_application.directory_simulation.navigation import navigation
from .find_next.full_progress import FullProgress
from .find_next.no_progress import NoProgress
from .watched_list import WatchedList


class ManageWatched:
    """Manages changing of the watch list when a video has been watched and creates and deletes thumbnails for the watched videos"""

    def __init__(self):
        """Sets up objects to find information about which video to watch next"""
        # finds the next file to add to the watched list
        self.find_next_full_progress = FullProgress()
        self.find_next_no_progress = NoProgress()

        # contains the watched list and methods to act on it
        self.watched_list = WatchedList()

        # checks if all in folder is full in order to set the folder above to full progress
        navigation.do_at_level(lambda: navigation.do_in_elements(self.set_progress_on_folders_above, include_folders=True), level=0)

    def set_progress_on_folders_above(self):
        """Check if all of the video files in the folder have been watched and set progress on folder accordingly"""

        current_folder = navigation.get_location()[:]
        level = len(current_folder)

        navigation.go_back_home()
        navigation.go_to_folder(current_folder[0])
        for i in range(1, level):
            if navigation.is_folder():
                navigation.go_to_folder(current_folder[i])
                fraction = navigation.get_progress_fraction_under()
                if fraction == 0:
                    navigation.set_progress(None)  # set progress on folder above the watched videos
                else:
                    navigation.set_progress(fraction)

    def before_watching(self):
        """Runs before program is watched in the case the video to watch is set to full progress. This runs to check
        that there are no "up next " items left over; if the current video is then set to unwatched or partly watched"""

        self.watched_list.clear_any_next_up()
        if navigation.get_progress() == 1.0:  # video has been watched
            navigation.set_progress(None)

    def finished_watching(self, progress):
        """Runs after program has been watched and handles what to do with the watched list based on the progress
        through the video file and the watched state of the other files in the series."""

        def do_for_progress_bounds(start, middle, end):
            """Run different methods based on how far into the video play has stopped"""
            if progress < 0.05:  # less then 5 percent of the way through the video file
                # if arguments are present pass to the function
                start()
            elif progress > 0.95:  # more than 95 percent of the way through the video file
                end()
            else:  # between these two values
                middle()

        def set_progress_for_bounds():
            """Set progress on video file based on the three progress bounds"""
            do_for_progress_bounds(lambda: navigation.set_progress(None), lambda: navigation.set_progress(progress), lambda: navigation.set_progress(1.0))

        def update_watched_start():
            """Find next video file and add it to the watched list if stopped at beginning of video"""
            next_file = self.find_next_no_progress.find()
            if next_file is not None:
                navigation.do_at_level(lambda : navigation.do_in_folder(self.watched_list.add_entry, next_file), 2)  # add the next video file to watched to the watched list

        def update_watched_end():
            """Find next video file and add it to the watched list if stopped at end of video"""

            next_file = self.find_next_full_progress.find()
            if next_file is None:
                navigation.do_at_level(lambda: self.watched_list.progress_wipe(safeguard=True, include_watched_list=True), 2)  # remove progress from watched video files
            else:
                navigation.do_at_level(lambda: navigation.do_in_folder(self.watched_list.add_entry, next_file), 2)  # add the next video file to watched to the watched list

        # if the finished watching video is in the watched list remove
        self.watched_list.remove_watched_thumbnail()

        # if in middle make thumbnail at current place
        do_for_progress_bounds(lambda: None, lambda: self.watched_list.make_watched_thumbnail(progress), lambda: None)
        # set the progress on the file
        do_for_progress_bounds(lambda: navigation.set_progress(None), lambda: navigation.set_progress(progress), lambda: navigation.set_progress(1.0))
        set_progress_for_bounds()

        if navigation.is_file_in_single_folder():  # if just one file in a folder
            # add or remove from watched list based on progress
            do_for_progress_bounds(self.watched_list.remove_entry, self.watched_list.add_entry, self.watched_list.remove_entry)
            navigation.go_back()
            set_progress_for_bounds()

        else:  # video is in a folder
            do_for_progress_bounds(self.watched_list.remove_entry, self.watched_list.add_entry, self.watched_list.add_entry)
            do_for_progress_bounds(update_watched_start, lambda : None, update_watched_end)

        navigation.go_back()
        self.watched_list.write_to_file()
        # check to see if all in the folder is full, if it is need to update the frame above
        self.set_progress_on_folders_above()

    def get_home_paths(self):
        """Get watched paths to display on home page"""
        return self.watched_list.get_home_paths()


manage = ManageWatched()
