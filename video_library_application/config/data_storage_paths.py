class DataStoragePaths:
    """Sets the paths that contains the saved files/folders required for the program"""

    # thumbnail folder locations
    thumbnail_parent =          "./data/thumbnails/"
    thumbnails =                thumbnail_parent + "fixed_position/"  # ordinary thumbnails
    progress_thumbnails =       thumbnail_parent + "part_watched/"  # thumbnails if part way through a video

    base_directories =          "./data/base_directories.txt"

    folder_structure_pickle =   "./data/folder_structure.pickle"
    watched_list_json =         "./data/watched_list.json"