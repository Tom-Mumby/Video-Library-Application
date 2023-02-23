from video_library_application.config.data_storage_paths import DataStoragePaths
import os


class RemoveThumbnails:
    """Contains information about thumbnails and contains methods to change them"""
    thumbnail_path = DataStoragePaths.thumbnails

    def __init__(self):
        """gets a list of thumbnails currently in the directory"""
        self.names = os.listdir(self.thumbnail_path)

    def matching(self, matches):
        """Removes all thumbnail names that do not have the matching part in them"""
        # list to contain matching names in
        list_matching = []
        for match in matches:
            for file_name in self.names:
                # if name matches
                if file_name.count(match) != 0:
                    list_matching.append(file_name) # add to matching list
        self.names = list_matching # set list of names to new matching names

    def delete_files(self):
        """Delete all thumbnail files in thumbnails names list"""
        if len(self.names) > 0:
            print("    ")
            print("---Deleting no longer needed thumbnails---")
        for name in self.names:
            print(name)
            os.remove(self.thumbnail_path + name)

    def check_exists(self, image_name):
        """If specific image name is in list of image names in list, remove from list and print config"""
        if image_name in self.names: # if image already exists
            print("\tThumbnail already exists")
            print("\t"+image_name)
            self.names.remove(image_name) # get rid of image from thumbnail file so can delete remaining at the end of the method
            return True
        else:
            return False
