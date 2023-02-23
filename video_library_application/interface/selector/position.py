from video_library_application.same_state import SameState
from video_library_application.array_point import ArrayPoint
from video_library_application.interface.selector.change_label_colour import ChangeLabelColour
from video_library_application.config.key_press import KeyPress

import threading


class Position:
    """Changes the selected item in a matrix of tkinter frames or labels to show which from the is currently selected"""

    def __init__(self, tkinter_elements_matrix, default_colour, selected_colour):
        """Sets the initial selected position"""

        self.tkinter_elements_matrix = tkinter_elements_matrix  # array of the frames
        self.matrix_size = ArrayPoint(row=len(self.tkinter_elements_matrix), column=len(self.tkinter_elements_matrix[0]))

        self.selected = ArrayPoint(0, 0)  # location of currently selected frame
        self.selected_old = ArrayPoint(0, 0)  # location of previously selected frame

        self.first_press = SameState()  # false if not been pressed
        self.colours = ChangeLabelColour(default_colour, selected_colour)

    def change_selected(self, key_code):
        """Changes the selected element based on which of the arrow keys has been pressed"""
        if self.first_press.is_still():  # if this is the first press
            self.colours.set_selected(self.tkinter_elements_matrix[0][0])  # change the boarder of the frame in the top left position
            self.first_press.is_not()
            return True  # true as has been updated

        self.selected_old.set(self.selected)  # set the current position

        # up pressed
        if key_code == KeyPress.up:
            if self.selected.row > 0:  # not on top row
                self.selected.row -= 1  # move row up by one
                return self.update_selected_colours()  # update boarder and return true is successful
        # left pressed
        if key_code == KeyPress.left:
            if self.selected.column > 0:  # not on left column
                self.selected.column -= 1  # move column to the left
                return self.update_selected_colours()  # update boarder and return true is successful
        # right pressed
        if key_code == KeyPress.right:
            if self.selected.column < self.matrix_size.column - 1:  # not in rightmost column
                self.selected.column += 1  # move column to the right
                return self.update_selected_colours()  # update boarder and return true is successful
        # down pressed
        if key_code == KeyPress.down:
            if self.selected.row < self.matrix_size.row - 1:  # not at bottom row
                self.selected.row += 1  # move row down by one
                return self.update_selected_colours()  # update boarder and return true is successful

        return None  # return none if not updated

    def update_selected_colours(self, do_fade=True):
        """Updates the colours of the selected and deselected elements"""

        def fade_selected():
            """Fades the colours of the elements"""
            self.colours.fade_labels(old_label=self.tkinter_elements_matrix[self.selected_old.row][self.selected_old.column],
                                     new_label=self.tkinter_elements_matrix[self.selected.row][self.selected.column])

        if self.matrix_size.column > 1 and self.tkinter_elements_matrix[self.selected.row][self.selected.column].is_blank():  # if the new selected frame is blank
            self.selected.set(self.selected_old)  # set the selected frame to the previous location
            return False  # as has not been changed
        else:
            if do_fade:
                threading.Thread(target=fade_selected).start()
            else:
                self.colours.set_default(self.tkinter_elements_matrix[self.selected_old.row][self.selected_old.column])  # set frame back to normal
                self.colours.set_selected(self.tkinter_elements_matrix[self.selected.row][self.selected.column])  # highlight background
            return True  # as has been changed


