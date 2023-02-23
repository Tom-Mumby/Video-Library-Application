from .directory_elements import Folder
from ..config.system_type import SystemType
from ..config.data_storage_paths import DataStoragePaths
from ..read_text_file import ReadTextFile

import pickle
from natsort import natsorted


class Navigation:
    """Class that creates a directory structure inside the program. Contains methods to move into and out of these
    folders and get information about the current location. Also contains methods to write the directory structure to
    the disk and read it back in."""

    folder_separator = SystemType.folder_sep  # folder separator for the system

    def __init__(self):
        # creates a home folder object, this will be the current folder as the location within the folder structure changes
        self.current_folder = Folder("home", "none")

        self.list_location = []  # a list containing the current location will go in here
        self.base_folders = ReadTextFile.do_read(DataStoragePaths.base_directories)  # get the base folders as a list

    def pickle_structure(self):
        """Writes the directory structure object to the disk"""
        def do_pickle():
            pickle_out = open(DataStoragePaths.folder_structure_pickle,"wb")  # serialises directory structure object to file
            pickle.dump(self.current_folder, pickle_out)
            pickle_out.close()

        self.do_at_level(do_pickle, 0)

    def unpickle_structure(self):
        """Reads the directory structure object from disk"""
        pickle_in = open(DataStoragePaths.folder_structure_pickle,"rb")  # reads object in
        self.current_folder = pickle.load(pickle_in)
        pickle_in.close()

    def print_current(self):
        """Prints current folder/file information to screen"""
        print("Current folder name     :" + self.current_folder.name)
        print("Location")
        print(self.list_location)

    def print_progress_info(self):
        """Prints information about the progress information at the current location"""
        def inner():
            level = self.get_level() - 2
            start = ""
            for i in range(level):
                start = start + "\t"

            print(start + str(self.get_progress()) + "\t" + self.current_folder.name)

        self.do_at_level(lambda: self.do_in_elements(inner, include_files=True, include_folders=True), 2)

    def add_folder(self, new_folder_name, go_in=False):
        """Adds folder at current location"""
        if go_in:  # if going into the folder
            self.current_folder = self.current_folder.new_folder(new_folder_name)  # update current location to be new folder
            self.list_location.append(new_folder_name)
        else:
            self.current_folder.add_folder(new_folder_name)  # just add new folder

    def add_file(self, video_name, readable_name):
        """Add new file at current location"""
        self.current_folder.new_file(video_name, readable_name)

    def remove_under(self):
        """Remove all of the directory structure under the current location"""
        self.current_folder.children.clear()

    def remove_folder(self, remove_name):
        """Remove a folder with a specified name"""
        children_names = self.get_children_names()  # get list of the names of the files/folders underneath current loaction
        index = children_names.index(remove_name)  # find the index of the file to remove
        del self.current_folder.children[index]  # remove the file/folder with that index

    def is_home(self):
        """Returns true if the current location is the home folder"""
        if self.get_level() == 0:
            return True
        else:
            return False

    def is_name(self, check_name):
        """Returns true if the current name is the same as the one being checked; false otherwise"""
        if check_name == self.current_folder.name:
            return True
        else:
            return False

    def is_folder(self):
        """Returns true if the is current location is a folder"""
        return self.current_folder.is_folder()

    def is_single_file_under(self):
        """Returns true if in a folder with a single file directly under it"""
        if self.is_folder():
            if self.get_num_children() == 1:
                if self.current_folder.children[0].is_folder() is False:
                    return True
        return False

    def is_file_in_single_folder(self):
        """Returns true if in a file with a single folder directly abouve it"""
        if self.is_folder() is False:
            file_name = self.current_folder.name
            self.go_back()
            is_true = self.is_single_file_under()
            self.go_to_folder(file_name)
            return is_true

    def is_only_files_below(self):
        """Returns true if the children of the current directory are all files"""
        for i in range(len(self.current_folder.children)):
            if self.current_folder.children[i].is_folder():
                return False
        return True

    def go_back(self, times=1):
        """Go up number of folders determined by times"""
        for i in range(0, times):
            del self.list_location[-1]  # remove the folder just left from the location list
            self.current_folder = self.current_folder.get_parent()  # go into the parent folder

    def go_back_home(self):
        """Resets current directory back to the home directory"""
        self.go_back(self.get_level())

    def go_to_folder(self, folder_name):
        """Go into specified folder or go through a list of folders"""
        def go_to(s_folder):
            """Go into folder"""
            # add to current location
            self.list_location.append(s_folder)
            # go into folders
            self.current_folder = self.current_folder.get_child(s_folder)

        if type(folder_name) is str: #if folder is string
            go_to(folder_name)
        else:
            for folder in folder_name: # if folder is list of folders
                go_to(folder)

    def go_to_folder_index(self, index):
        """Go into the folder directly under the current one with the index"""
        self.current_folder = self.current_folder.children[index]  # go into folder with index
        self.list_location.append(self.current_folder.name)  # add current folder to location list

    def go_to_level(self, level):
        """Go the level numbered from the top level as 0"""
        self.go_back(len(self.list_location) - level)

    def do_in_folder(self, method_in_folder, path_to_folder_list):
        """Run method inside a given folder"""
        assert type(path_to_folder_list) is list
        self.go_to_folder(path_to_folder_list)
        method_in_folder()
        self.go_back(len(path_to_folder_list))

    def do_in_elements(self, func, include_files=False, include_folders=False):
        """Runs function in every file in file structure. Have to start in folder"""
        for i in range(self.get_num_children()):
            self.go_to_folder_index(i)
            if self.is_folder():  # is folder
                if include_folders:
                    func()
                self.do_in_elements(func, include_files, include_folders)
            else: # is file
                if include_files:
                    func()

            self.go_back()

    def do_at_level(self, method_at_level, level, *args):
        """Run method at a chosen level"""
        current_path = self.list_location[level:]

        self.go_to_level(level)
        method_at_level(*args)
        self.go_to_folder(current_path)

    def sort_children(self):
        """Sort children in alphabetical order"""
        sort_by = self.get_children_names()  # get list of child names to sort by
        order = [i for i in range(len(sort_by))]  # get list of integers

        zipped_lists = zip(sort_by, order)  # zip into tuple
        zipped_lists = natsorted(zipped_lists)  # sort tuple using package to ensure correct readable order

        order = [element for _, element in zipped_lists]  # extract order from tuple

        #  checks if the order of the list has changed
        num_matching = 0
        for i in range (len(sort_by)):
            if i == order[i]:
                num_matching += 1
        if num_matching == len(sort_by): # no element have changed position
            return
        self.current_folder.children = [self.current_folder.children[i] for i in order]  # reorder children

    def sort_children_under(self):
        """Recursively alphabetise the folders under the current location"""
        def inner():
            if self.is_home() is False:
                self.sort_children()
                if self.is_only_files_below():
                    for i in range(len(self.current_folder.children)):
                        self.current_folder.children[i].display_name = "Episode " + str(i+1) + self.current_folder.children[i].display_name

        if self.is_only_files_below():
            inner()
        else:
            self.do_in_elements(inner, include_files=False, include_folders=True)

    def set_progress(self, progress):
        """Sets the value for the progress on element"""
        self.current_folder.progress = progress

    def get_current_name(self):
        """Returns the name of the element at the current location"""
        return self.current_folder.name

    def get_level(self):
        """Returns the folder level down from the top folder"""
        return len(self.list_location)

    def get_progress(self):
        """Returns the progress, has to be a file to do this"""
        return self.current_folder.progress  # works as long as are calling method on a file

    def get_children_names(self):
        """Returns a list of the names of the files/folders directly under the current location"""
        names_list = []  # list to put names in
        for i in range(len(self.current_folder.children)):  # adds names to list
            names_list.append(self.current_folder.children[i].name)
        return names_list

    def get_num_children(self):
        """Returns the number of files/folders directly under the current directory"""
        return len(self.current_folder.children)

    def get_num_files_under(self):
        """Returns the number of files at the current location"""

        def add_one():
            nonlocal total_number
            total_number += 1

        total_number = 0
        self.do_in_elements(add_one, include_files=True)
        return total_number

    def get_progress_fraction_under(self):
        """Returns the average progress of the video files under the current location"""

        def check_file():
            """Checks progress on video file and increments the total numbers of files"""

            nonlocal files_watched
            nonlocal total_number_files

            progress = self.get_progress()
            if progress is not None:  # watched in some way
                files_watched += progress
            total_number_files += 1

        total_number_files = 0
        files_watched = 0

        self.do_in_elements(check_file, include_files=True)

        # returns watched fraction
        return files_watched / total_number_files

    def get_location(self):
        """Returns the folders traversed in order to reach the current folder and the name of the current folder as a list"""
        return self.list_location

    def get_path(self, separator, start=0, end=0):
        """Returns the path of the current location as a string with a chosen separator"""
        path_string = ""
        for i in range(start, len(self.list_location)-end):  # add each element from path to the string
            if i != start:
                path_string = path_string + separator  # if not at the first element in the string add the separator
            path_string = path_string + self.list_location[i]  # add the next path element to the string

        return path_string

    def add_additional_path(self, separator, path):
        """Adds any additional path string to the video location string if it is present in the element"""
        if self.is_folder() is False:  # if at file
            additional_path = self.current_folder.additional_path  # get additional path
            if additional_path:
                if type(additional_path) is str:
                    path = path + separator + additional_path
                else:
                    for path_part in additional_path:
                        path = path + separator + path_part
        return path

    def get_full_path(self):
        """Returns the full system path at the current location"""
        location_string = ""
        for base_folder in self.base_folders:  # loop over the base folders to see which ones match
            start_folder = base_folder.split(self.folder_separator)[-1]  # get the last part of the base folders
            if start_folder == self.list_location[0]:  # check if matches the first part of the list location
                location_string = base_folder  # set return string at the correct base directory
                break

        if self.get_level() > 1:  # if past first directory add this part to the base folder string
            location_string = location_string + self.folder_separator + self.get_path(self.folder_separator, 1)

        location_string = self.add_additional_path(self.folder_separator, location_string)

        return location_string

    def get_image_location(self):
        """Returns the thumbnail path for a given file or folder, if at a folder go into the top directories until a file is reached"""

        image_path = ""
        if self.is_folder():  # if in folder
            count = 0  # count number of directories entered

            while self.current_folder.is_folder():  # while still in a folder
                count += 1
                self.go_to_folder_index(0)  # go into top folder

            image_path = image_path + self.get_path("_")  # set image path
            image_path = self.add_additional_path("_", image_path)
            # add get alternate image here if not available
            for _ in range(count):  # go back to start location
                self.go_back()
        else:  # if in file
            image_path = image_path + self.get_path("_")  # set image path
            image_path = self.add_additional_path("_", image_path)

        return image_path + ".jpg"


# creates the file/folder navigation object
navigation = Navigation()
