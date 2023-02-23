from video_library_application.config.key_press import KeyPress
from video_library_application.prepare import scan_files_on_disk
from video_library_application.watched import manage_watched
from video_library_application.interface.selector.position import Position


class MenuPosition(Position):
    """Handles changing the selected item in the menu and what happens when an item is pressed"""

    def __init__(self, menu_list, labels_matrix, default_colour, selected_colour):
        """Creates reference to the menu frame and the text"""

        super().__init__(labels_matrix, default_colour, selected_colour)

        self.menu_list = menu_list
        self.label_text = self.menu_list.button_text

    def change_position(self, key_code):
        """Changes the position of the menu and actions what the user had decided to do when they press enter"""

        # only allow a subset of the keys
        if key_code not in [KeyPress.up, KeyPress.down, KeyPress.enter, KeyPress.back, KeyPress.menu_or_subtitles]:
            return None
        # if needed changes the selected item in the menu
        self.change_selected(key_code)

        if key_code == KeyPress.enter:  # if the user desires an action

            # text to match
            selected_text = self.tkinter_elements_matrix[self.selected.row][0].cget("text")

            # wipe progress on videos below
            if selected_text == self.label_text[2]:
                manage_watched.manage.watched_list.clear_any_next_up()
                if manage_watched.manage.watched_list.progress_wipe(safeguard=True, include_watched_list=True):
                    manage_watched.manage.set_progress_on_folders_above()
                    return True  # reload frames
            # exit the program
            elif selected_text == self.label_text[3]:
                exit()
            else:
                self.menu_list.make_progress_bar()

                # scan all files
                if selected_text == self.label_text[0]:
                    scan_files_on_disk.scan_files_on_disk.update_from_location(compare_top=False, menu_bar=self.menu_list.progress_bar) # update all folders under
                # scan top folders for changes
                elif selected_text == self.label_text[1]:
                    scan_files_on_disk.scan_files_on_disk.update_from_location(compare_top=True, menu_bar=self.menu_list.progress_bar)  # check if the top level folders are different and then update
                manage_watched.manage.__init__()
                return True

        # remove the menu from the screen
        elif key_code == KeyPress.back or key_code == KeyPress.menu_or_subtitles:
            return False
