from video_library_application.directory_simulation.navigation import navigation
from video_library_application.config.data_storage_paths import DataStoragePaths
from video_library_application.watched import manage_watched
from .blank_data import BlankData


class ThumbnailData(BlankData):
    """Contains data to make a thumbnail with label sub-frame. It chooses the next up thumbnail for folders above bottom directory"""

    def __init__(self):

        def partially_watched(progress="DEFAULT"):
            if progress == "DEFAULT":
                progress = self.progress

            if progress is None or progress == 1:
                return False
            else:
                return True

        super().__init__()
        self.progress = navigation.current_folder.progress
        if navigation.is_folder():  # if currently at a folder
            self.name = navigation.current_folder.name
        else:  # if currently at a file
            self.name = navigation.current_folder.display_name

        output_path = DataStoragePaths.thumbnails
        watched_path = navigation.get_image_location()

        if navigation.is_folder():
            if partially_watched():# progress thumbnail exists
                # find matching in the watch list
                # if none exists have a look
                watched_path_list = manage_watched.manage.watched_list.get_matching_watched(navigation.get_location())
                if watched_path_list is None:
                    watched_path_list = manage_watched.manage.find_next_no_progress.find()
                navigation.go_to_folder(watched_path_list)
                watched_path = navigation.get_image_location()
                if partially_watched(navigation.get_progress()):
                    output_path = DataStoragePaths.progress_thumbnails
                navigation.go_back(len(watched_path_list))

        else:  # is file
            if partially_watched():  # progress thumbnail exists
                output_path = DataStoragePaths.progress_thumbnails

        self.thumbnail_path = output_path + watched_path