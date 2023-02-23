class MenuControl:
    """Controls the menu that sits within the full-screen frames, contains methods to: show, remove, and update the menu"""

    def __init__(self, frames):
        """Sets lists of frames and set a variable to indicate it is not yet showing"""
        self.frames = frames
        self.showing = False

    def is_showing(self):
        """Returns true if the menu is currently showing on the current frame"""
        return self.showing

    def add_menu(self, frame):
        """Adds menu to the current frame"""
        frame.add_menu()
        self.showing = True

    def remove_menu(self):
        """Removes menu from the current frame"""
        self.frames.get_last().remove_menu()
        self.showing = False

    def keypress_menu(self, key_code):
        """Handles if any keys are entered when the menu is showing"""

        menu_return = self.frames.get_last().menu_list.position.change_position(key_code)
        if menu_return is not None:
            self.frames.get_last().remove_menu()
            self.showing = False
            return menu_return # update frames if true
