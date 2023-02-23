from video_library_application.config.system_type import SystemType
from video_library_application.directory_simulation.navigation import navigation
from .thumbnails.remove_thumbnails import RemoveThumbnails
from ..same_state import SameState
from .report_issues import ReportIssues
from .search_files import SearchFiles

import os


class ScanFilesOnDisk:
    """Scans folders and files on disk and updates the directory structure saved within the programme.
    Can rescan from any starting folder and scan all folders or just the top folders for changes"""
    folder_separator = SystemType.folder_sep

    @classmethod
    def update_from_location(cls, compare_top=False, menu_bar=False):
        """Updates thumbnail files and content file containing the folder structure"""

        def check_top_folders():
            """If comparing top folders for changes, set new update folders"""
            # set update path
            string_path = navigation.get_full_path()
            # set folders in path on network drive
            top_folders_on_drive = os.listdir(string_path)
            print("Top level folders on drive")
            print(top_folders_on_drive)
            # set folders in object
            top_folders_in_content = navigation.get_children_names()
            print("Top level top folders in application")
            print(top_folders_in_content)
            # put the extra folders that appear on drive but not in content file
            extra_on_drive = []
            # put the extra folders that appear in object but not on drive
            extra_in_object = []

            # loop over the folders on the network drive
            for folder in top_folders_on_drive:
                # if the folder is not in object add to extra on network drive list
                if folder not in top_folders_in_content:
                    extra_on_drive.append(folder)
            # loop over folders in content file
            for folder in top_folders_in_content:
                # if the folder is not on network drive add to extra in content file list
                if folder not in top_folders_on_drive:
                    extra_in_object.append(folder)
            if len(extra_in_object) > 0:
                print("Folders in application but not on drive")
                print(extra_in_object)
            if len(extra_on_drive) > 0:
                print("Folders on drive but not in application")
                print(extra_on_drive)
            scan_folders = []
            # add new update folders so can run update content file and thumbnails under
            for extra in extra_on_drive:
                scan_folders.append(string_path + cls.folder_separator + extra)
            thumb_matches = []
            # for extra folders in content file
            for extra_folder in extra_in_object:
                # removes unwanted part of object
                navigation.remove_folder(extra_folder)
                # delete extra thumbnails
                thumb_matches.append(navigation.get_path("_") + "_" + extra_folder + "_")

            remove_thumbnails.matching(thumb_matches)
            print("Folders to update")
            print(scan_folders)
            return scan_folders

        # any odd results in to be printed at the end
        report = ReportIssues()
        # controls which thumbnails to remove from system
        remove_thumbnails = RemoveThumbnails()

        folders = []  # put list of paths to update to in here
        if navigation.is_home(): # in top directory
            folders = navigation.base_folders  # set folders to update to be the base directory folders
            navigation.remove_under()  # remove directory structure under current location
        elif compare_top: # comparing top folders in directory for changes
            folders = check_top_folders()  # run method to compare top folders
        else:  # updating structure under folder not in top directory
            folders.append(navigation.get_full_path())  # get the full path of the current directory
            navigation.remove_under()   # remove directory structure under current location
            remove_thumbnails.matching([navigation.get_path("_")])  # only keep thumbnails that match the current location

        if menu_bar:
            menu_bar.get_total_folder_number(folders)


        # for the list of folders to update
        for folder in folders:
            nav_level = navigation.get_level()  # get the current depth into the folder structure
            folder_path_level = folder.count(cls.folder_separator)
            path_level = 0  # set an initial value for the level of the folder according to the full path
            first_file = SameState()
            if os.path.isdir(folder) is False: # check folder exists on system
                print("Folder does not exist, please edit the directory file")


            # check folder exists on system
            # go into all the folders under the update path
            for (path, dirs, files) in os.walk(folder, topdown=True):
                # print current path
                print(path)
                # get the last part of the path
                new_folder = path.split(cls.folder_separator)[-1]

                first_folder = False

                if path == folder and navigation.is_name(new_folder):  # if at the first folder
                    print("Skip adding folder")  # don't add so continue to next loop
                    first_folder = True
                else:
                    # pass to menu to update
                    if (folder_path_level + 1 == path_level or path_level == 0) and menu_bar is not False:
                        menu_bar.update_progress()
                    level_difference = 1 + path_level - path.count(cls.folder_separator)  # find the difference in level between now and the end of the last loop
                    if level_difference > 0:  # if this difference is positive, implies that the next folder is above the previous go back to it
                        navigation.go_back(level_difference)

                    navigation.add_folder(new_folder, go_in=True)  # add new folder and enter it
                    path_level = path.count(cls.folder_separator)  # get the level of the folder according to the full path

                if len(dirs) == 0: # if at bottom folder
                    if len(files) == 0: # if no files in folder
                        report.write_error("Empty folder at:",path)
                        print("As a result exiting script")
                        exit()
                    else: # if there are files in the folder
                        # handle list of found video files
                        SearchFiles.handle_files(files, path, remove_thumbnails, report, first_folder, menu_bar)

                        if compare_top and first_file.is_still():  # if at the first file and are comparing top files, add to watching list
                            if navigation.is_folder():  # if at folder
                                navigation.go_to_folder_index(0)  # go into top file
                                from video_library_application.watched import manage_watched
                                manage_watched.manage.watched_list.add_entry()  # add to watched
                                navigation.go_back()  # go back to folder
                            else:
                                navigation.watched.add_entry()  # add to watched
                            first_file.is_not() # set to false so does not add any more in this folder to watched

            # go back to starting folder location
            navigation.go_back(navigation.get_level() - nav_level)

        # sort the folders alphabetically
        if compare_top:  # if comparing the the folders
            navigation.sort_children()  # sort top level children
            for folder_path in folders:  # for each updated folder
                print(folder_path.split(cls.folder_separator)[-1])
                navigation.print_current()
                navigation.do_in_folder(navigation.sort_children_under, [folder_path.split(cls.folder_separator)[-1]]) # path must be list
        else:
            navigation.sort_children_under()  # sort recursively all of the children

        # add episode tags to files

        # delete any obsolete thumbnail files
        remove_thumbnails.delete_files()

        # print any errors that may have occurred
        report.print_report()

        # write new structure to file
        navigation.pickle_structure()


scan_files_on_disk = ScanFilesOnDisk()

