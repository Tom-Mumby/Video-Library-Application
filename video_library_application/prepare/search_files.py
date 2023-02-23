from video_library_application.config.system_type import SystemType
from video_library_application.config.data_storage_paths import DataStoragePaths
from video_library_application.directory_simulation.navigation import navigation
from .thumbnails import make_thumbnail


class SearchFiles:
    """Contains a method that runs when at a bottom folder which may contain video files to add these files to the
    navigation object """

    video_extensions = [".flv", ".mkv", ".avi", ".wmv", ".mov", ".mp4", ".m4p", ".m4v", ".mpg", ".mp2", ".mpeg",
                        ".mpe", ".mpv", ".mpg", ".mpeg", ".m2v", ".divx", ".ogm", ".webm"]


    @classmethod
    def handle_files(cls, files, path, thumbnail_list, report, first_folder, menu_bar):
        """When in bottom folder look through files to find video files, add file to content list and creates thumbnail"""

        # list to put the names of the video files in
        video_names = []

        # loop of the files in folder
        for i in range(len(files)):
            # get the file extension
            extension = files[i].split(".")
            extension = "." + extension[-1]
            # if the extension is a video file extension
            if extension.lower() in cls.video_extensions:
                # add video file name to list
                video_names.append(files[i])

        if len(video_names) == 0: # if no video files in directory
            report.write_error("No video files in:", path)
            print("As a result exiting script")
            exit()
            #return

        # convert video files to readable names
        readable_names = cls.convert_name(video_names)

        # sort out thumbnails
        for i in range(len(video_names)):
            if first_folder:
                menu_bar.update_progress()
            # add video file names to content to update
            navigation.add_file(video_names[i], readable_names[i])

            # could go into file here to generate image name

            # make name of image
            image_name = navigation.get_path("_") + "_" + video_names[i] + ".jpg"

            if thumbnail_list.check_exists(image_name) is False: # if thumbnail file does not exist
                try:
                    # create thumbnail get the cropped dimensions of the image
                    if make_thumbnail.ThumbnailMake.generate_thumbnail(path + SystemType.folder_sep + video_names[i], DataStoragePaths.thumbnails + image_name):
                        print("\t"+image_name)
                    else:
                        report.write_error("Thumbnail not made", path, "\t" + image_name)

                except FileNotFoundError:
                    report.write_error("Could not open video file", path, image_name)

    @staticmethod
    def convert_name(names):
        """Convert video file names to readable format"""
        def remove_matching(b_start):
            """Finds index upto which all of elements in the list match, starting from the start if b_start is true otherwise starting from the end"""
            # select string to compare from first filename and convert to lowercase so is not case sensitive
            string_compare = raw_names[0].lower()
            # loop over length of compare string
            while len(string_compare) > 1:
                # loops over all of the raw names
                for j in range(1, len(raw_names)):
                    # sets current name to compare with and coverts to lowercase so is not case sensitive
                    current_name = raw_names[j].lower()
                    # if checking from start of string
                    if b_start:
                        # if the start of the string doesn't match the compare string
                        if not current_name.startswith(string_compare):
                            # remove character from end of compare string and break loop
                            string_compare = string_compare[:-1]
                            break
                    # if checking from end of string
                    else:
                        # if the end of the string doesn't match the compare string
                        if not current_name.endswith(string_compare):
                            # remove character from start of string and break look
                            string_compare = string_compare[1:]
                            break
                    # when at end of loop return length of matching string part
                    if j == len(raw_names) - 1:
                        return len(string_compare)
            # if nothing found return matching lenght of zero
            return 0

        # if only one name in list return
        if len(names) == 1:
            return names
        # create list of the raw names
        raw_names = []
        for name in names:
            raw_names.append(name)

        # loop over raw names
        for i in range(len(raw_names)): # remove file extension
            # loop over letters in each raw name starting from end
            for j in range(len(raw_names[i])-1, 0, -1):
                if raw_names[i][j] == ".": # when first dot find indicating end of extension
                    raw_names[i] = raw_names[i][:j] # set new name without file extension
                    break
        # get number of characters at start of string to cut
        cut_length = remove_matching(True)
        # cut characters at the start of the string
        for i in range(len(raw_names)):
            raw_names[i] = raw_names[i][cut_length:]
        # get number of characters at the end of the string to cut
        cut_length = remove_matching(b_start=False)
        # remove characters at the end of the string
        for i in range(len(raw_names)):
            raw_names[i] = raw_names[i][:len(raw_names[i])-cut_length]

        # list to put lists of words from names in
        list_names = []
        # loop over raw names
        for raw_name in raw_names:
            # replace any characters that may be standing in for space
            strip_name = raw_name.replace("-"," ")
            strip_name = strip_name.replace(".", " ")
            strip_name = strip_name.replace("_", " ")
            # split into list using space as delimiter
            strip_name = strip_name.split(" ")

            # loop over words in this list
            i = 0
            while i < len(strip_name):
                # if word is blank remove
                if strip_name[i] == "":
                    del strip_name[i]
                    i -= 1
                else:
                    # loop over characters in work
                    for character in strip_name[i]:
                        # if there is a number in the word remove from list
                        if character.isdigit():
                            del strip_name[i]
                            i -= 1
                            break
                i += 1
            # add new name list to list of names
            list_names.append(strip_name)
        # list to put formatted names in
        formatted_names = []

        # loop over new list of name lists
        for i in range(0, len(list_names)):
            # set episode number based on position in list
            path_string = ""
            # loop over list comprising name
            for j in range(0, len(list_names[i])):
                # if not first element separate words by space
                if j != 0:
                    path_string = path_string + " "
                else: # if first put a dash in to mark if all from episode part of string
                    path_string = path_string + " - "
                # add last element of list to string
                path_string = path_string + list_names[i][j]

            formatted_names.append(path_string)

        return formatted_names
