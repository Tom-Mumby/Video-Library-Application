from video_library_application.config.data_storage_paths import DataStoragePaths

import os


class PrerequisiteFilesCheck:
    """Checks necessary folders are in place and contains a method to update the stored data"""

    # check for file containing locations of video files
    if not os.path.isfile(DataStoragePaths.base_directories):
        print("There is no file containing the base directories to search for the video files in.\nPlease create the file\n"
              + DataStoragePaths.base_directories
              + " \ncontaining the folders where your video files are stored, with each folder listed on a new line, then rerun the program.\n\n"
              +  "Alternatively you can enter them below.")
        added_folders = []
        while True:
            entered_text = input("Enter folder or enter \"y\" to finish entries.\n")
            if entered_text == "y":
                if len(added_folders) == 0:
                    print("No folders entered, exiting program")
                    exit()
                else:
                    print("Folders added, writing them to file.")
                    with open(DataStoragePaths.base_directories, 'w') as f:
                        for folder in added_folders:
                            f.write(f"{folder}\n")
                    break
            elif os.path.isdir(entered_text):
                added_folders.append(entered_text)
                print("Folder added")
            else:
                print("Folder not found, please try again")
    from .scan_files_on_disk import ScanFilesOnDisk
    # if file containing video config is not there
    if not os.path.isfile(DataStoragePaths.folder_structure_pickle):
        # ask user if they would like to continue
        print("There is no file containing the folder structure. Would you like to create one?")
        entered_key = input("Enter \"y\" to continue.\n")
        if entered_key == "y": # if continuing
            # make thumbnail folders
            if not os.path.isdir(DataStoragePaths.thumbnail_parent):
                os.mkdir(DataStoragePaths.thumbnail_parent)
            if not os.path.isdir(DataStoragePaths.thumbnails):
                os.mkdir(DataStoragePaths.thumbnails)
            if not os.path.isdir(DataStoragePaths.progress_thumbnails):
                os.mkdir(DataStoragePaths.progress_thumbnails)
            # run update all folders
            ScanFilesOnDisk.update_from_location()
        else: # exit script it not continuing
            print("Exiting")
            exit()
    else:  # if file containing video information is there
        from video_library_application.directory_simulation.navigation import navigation
        navigation.unpickle_structure()


PrerequisiteFilesCheck()
