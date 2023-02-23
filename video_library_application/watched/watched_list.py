from ..prepare.thumbnails import make_thumbnail
from video_library_application.config.data_storage_paths import DataStoragePaths
from video_library_application.directory_simulation.navigation import navigation

import json
import os


class WatchedList:
    """Contains the watched videos list and has methods to initilise from saved json and to add or remove videos from
    the list. This is done based off what the current folder is in the navigation object."""

    def __init__(self):
        """Removes any progress set in navigation and adds videos to the watched list based on entries in a json file"""
        self.watched_info_list = []  # list to put the watched video files info in

        def run_update():
            self.progress_wipe(safeguard=False, include_watched_list=False) # wipes progress in navigation simulation
            # write wiped structure to file in case any unwiped data has been saved during scan for new files
            navigation.pickle_structure()

            write_to_file = False
            j = 0
            while j < len(self.watched_info_list):  # loop over watched video files
                path = self.watched_info_list[j]['path']  # gets watched video path
                for i in range(len(path)):  # loops over folders in path
                    if path[i] in navigation.get_children_names():  # if folder is there
                        navigation.go_to_folder(path[i])  # go into folder
                    else:  # folder does not exist
                        del self.watched_info_list[j]  # remove from watched list
                        write_to_file = True  # rewrite watched file
                        if j > 0:
                            j -= 1
                    if i == len(path) - 1:  # at end of path
                        progress = self.watched_info_list[j]['progress']
                        navigation.set_progress(progress)  # set progress
                        if navigation.is_file_in_single_folder():
                            if 0.05 < progress < 0.95:  # in middle of video
                                navigation.do_at_level(navigation.set_progress, navigation.get_level()-1, progress)

                navigation.go_to_level(0)  # go back to home folder
                j += 1
            if write_to_file:  # if item deleted from watched list, rewrite watched json file
                self.write_to_file()

        self.watched_info_list.clear()
        if os.path.isfile(DataStoragePaths.watched_list_json):  # if previously watched data exists
            with open(DataStoragePaths.watched_list_json, 'r', encoding='utf-8') as f:  # load data
                self.watched_info_list = json.load(f)

        navigation.do_at_level(run_update, level=0)  # runs from home folder

    def print_list(self):
        for item in self.watched_info_list:
            print(item)

    def write_to_file(self):
        """Write watched list to file"""
        with open(DataStoragePaths.watched_list_json, 'w', encoding='utf-8') as f:
            json.dump(self.watched_info_list, f, ensure_ascii=False, indent=2)

    def get_index_in_list(self):
        """Return index of video in watched list if the same as current location in the navigation object"""
        check_path = navigation.get_location()[:]
        for i in range(len(self.watched_info_list)):
            if self.watched_info_list[i]["path"] == check_path:  # compare the two lists
                return i
        return None

    def remove_entry(self, delete_thumbnail=False):
        """Remove video file at the current navigation object location from the watched list"""
        index = self.get_index_in_list()
        if index is not None:
            if self.watched_info_list[index]["progress"] is None:
                return
            if delete_thumbnail:
                self.remove_watched_thumbnail()
            del self.watched_info_list[index]

    def add_entry(self):
        """Add new entry to top of watched list based on location in navigation object"""
        new_path = navigation.get_location()[:]
        self.remove_entry()
        self.watched_info_list.insert(0, {"path": new_path, "progress": navigation.get_progress()})  # need display name?


    def get_home_paths(self):
        """Get the file locations of the videos in the watched list to display on home page"""
        home_paths = []  # list to put paths in
        for i in range(len(self.watched_info_list)):  # add all paths to this list
            home_paths.append(self.watched_info_list[i]["path"])

        i = 0
        while i < len(home_paths):  # loop over all of the paths
            compare = home_paths[i][1]  # set part of path to compare to be the series name
            j = i + 1
            while j < len(home_paths):  # check each path after the current to see if they match
                if compare == home_paths[j][1]:  # path matches
                    del home_paths[j]  # remove path
                    j -= 1
                j += 1
            i += 1
        return home_paths

    def get_progress(self, index):
        """Get the progress of any entry in the watched list based on it's index"""
        return self.watched_info_list[index]["progress"]

    def get_matching_watched(self, path):
        """Return any watched videos that are under the path specified"""

        path_length = len(path)

        for entry in self.watched_info_list:
            if entry["path"][:path_length] == path:
                return entry["path"][path_length:]
        return None

    def progress_wipe(self, safeguard=True, include_watched_list=False):
        """Wipe the video files progress at the current location"""

        def set_to_false():
            """set progress to false and can remove from watched list"""
            if navigation.get_progress() is not None:
                navigation.set_progress(None)
                if include_watched_list and navigation.is_folder() is False:  # if selected remove from watched list
                    self.remove_entry(delete_thumbnail=True)

        if safeguard and navigation.get_level() < 2:  # if safeguard in place do not run if the level is too high
            return False  # no need for update

        navigation.do_in_elements(set_to_false, include_files=True, include_folders=True)
        if include_watched_list:
            self.write_to_file()
        return True  # to show update needed

    def clear_any_next_up(self):
        """Remove any next up under the location the navigation object is currently at"""
        top_path = navigation.get_location()[:2]
        i = 0
        while i < len(self.watched_info_list):
            if self.watched_info_list[i]["path"][:2] == top_path:
                if not self.watched_info_list[i]["progress"]:
                    del self.watched_info_list[i]
                    i -= 1
            i += 1

    def make_watched_thumbnail(self, progress):
        """Make watched thumbnail based on the current location and progress"""
        make_thumbnail.ThumbnailMake.generate_thumbnail(navigation.get_full_path(), DataStoragePaths.progress_thumbnails + navigation.get_image_location(), thumbnail_fraction=progress)

    def remove_watched_thumbnail(self):
        """Remove watched thumbnail if there is one at the current location of the navigation object"""

        index = self.get_index_in_list()
        if index is not None and 0 < self.watched_info_list[index]["progress"] < 1:
            os.remove(DataStoragePaths.progress_thumbnails + navigation.get_image_location())
