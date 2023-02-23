"""Contains the file and folder classes which are used in the directory structure, these inherit from the general Element Class"""


class Element:
    """Class with attributes and methods common to files and folders"""
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.progress = None

    def get_parent(self):
        """Returns the parent folders of the current element"""
        return self.parent

    def is_folder(self):
        """returns true if current type is a folder"""
        if type(self).__name__ == "Folder":
            return True
        if type(self).__name__ == "File":
            return False


class File(Element):
    """File class"""
    def __init__(self, name, display_name, parent, additional_path, progress):
        super().__init__(name, parent)
        self.additional_path = additional_path  # part to add to end of path if needed to locate file
        self.display_name = display_name  # name to display
        self.progress = progress  # progress through video file


class Folder(Element):
    """Folder class"""
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.children = []  # list to contain folders children

    def new_file(self, file_name, display_name, additional_path=None, progress=None, insert_index=-1):
        """Creates new file"""
        new_file = File(file_name, display_name, self, additional_path, progress)  # new file object
        if insert_index == -1:  # append to end of children list
            self.children.append(new_file)
        else:
            self.children.insert(insert_index, new_file)  # insert at index

    def new_folder(self, folder_name):
        """Creates new folder and returns it"""
        self.children.append((Folder(folder_name, self)))
        return self.children[-1]

    def get_child(self, child_name):
        """return child file/folder that has name"""
        for i in range(len(self.children)):
            if self.children[i].name == child_name:
                return self.children[i]

    def get_top_child(self):
        """returns the first child under folder"""
        return self.children[0]
