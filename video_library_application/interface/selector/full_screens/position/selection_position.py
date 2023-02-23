from video_library_application.config.key_press import KeyPress
from video_library_application.array_point import ArrayPoint
from ...position import Position


class GridPosition(Position):
    """Handles changing boarders on the frames within the selection frame and changing which sub-frames are displayed"""

    class LetterJump:
        """Jumps to first folder starting with the letter on the keypad"""

        # sets number of letters on eah key in keypad
        num_letters_keypad = [0] * 10
        num_letters_keypad[0] = 0
        num_letters_keypad[1] = 0
        num_letters_keypad[2] = 3
        num_letters_keypad[3] = 3
        num_letters_keypad[4] = 3
        num_letters_keypad[5] = 3
        num_letters_keypad[6] = 3
        num_letters_keypad[7] = 4
        num_letters_keypad[8] = 3
        num_letters_keypad[9] = 4

        # creates array containing the sum of the number of letters in the keypad
        sum_letters_keypad = [0]
        count = 0
        for number in num_letters_keypad:
            count += number
            sum_letters_keypad.append(count)

        def __init__(self, frame_data):
            # get a list of all of the folder names
            self.list_names = []
            for i in range(len(frame_data)):
                for j in range(len(frame_data[i])):
                    frame_name = frame_data[i][j].get_name()
                    if frame_name is not None and frame_name.isspace() is False:
                        self.list_names.append(frame_data[i][j].get_name())

            self.previously_pressed = -1
            self.letter_shift = 0

            # creates array containing the number of names which start with each letter of the alphabet
            self.number_starts_with_letter = [0] * 26
            for i in range(len(self.list_names)):
                start_letter = self.list_names[i][0].lower()
                if start_letter.isalpha():  # is letter
                    self.number_starts_with_letter[ord(start_letter) - 97] += 1  # add one to the correct array element, ord gives a number the corresponds to the letter
                else:
                    self.number_starts_with_letter[0] += 1
            # creates an array of the running total that starts with each letter
            self.total_starts_with_letter = [0]
            count = 0
            for number in self.number_starts_with_letter:
                count += number
                self.total_starts_with_letter.append(count)

        def get_index(self, pressed): # reset when leaving frame
            """get index to jump to"""
            def do_shift():
                """shift to next letter, if gone past last letter on keypad reset to 0"""
                self.letter_shift += 1
                if self.letter_shift >= self.num_letters_keypad[pressed]:
                    self.letter_shift = 0

            letter_number = self.sum_letters_keypad[pressed] # a is 0, z is 25
            if pressed == self.previously_pressed:  # if pressed the same letter, shift to next
                do_shift()
                for i in range(self.num_letters_keypad[pressed]):
                    # if there are no names that start with that letter look for next
                    if self.number_starts_with_letter[letter_number + self.letter_shift] == 0:
                        do_shift()
                    else:
                        break

            else:
                self.letter_shift = 0

            self.previously_pressed = pressed  # set last pressed
            letter_number += self.letter_shift  # add shift to letter number
            index = self.total_starts_with_letter[letter_number]  # get letter index
            if index == len(self.list_names):
                return None
            return index

    def __init__(self, frames_matrix, frame_data, arrows, default_colour, selected_colour):
        """Adds the two sets of arrows and sets the positions of the top and bottom rows"""
        super().__init__(frames_matrix, default_colour, selected_colour)
        self.frame_data = frame_data  # sets the data within the frame
        self.arrows = arrows
        self.letter_jump = self.LetterJump(frame_data)  # handles jump to letter
        self.position = 0  # sets initial vertical scrolling position
        self.max_position = len(self.frame_data) - self.matrix_size.row # maximum vertical scrolling position

        self.arrows.reset_arrows(self.can_scroll_down())  # set the starting colours for the scrolling arrows

    def can_scroll_down(self):
        """Checks if possible to scroll down"""
        if self.position < self.max_position:
            return True
        else:
            return False

    def change_position(self, key_code):
        """Changes the vertical scrolling position"""

        if key_code not in [KeyPress.up, KeyPress.left, KeyPress.right, KeyPress.down] and key_code not in KeyPress.numbers:
            return  # if not one of the arrow keys

        self.selected_old.set(self.selected)
        if key_code in KeyPress.numbers:  # if a number has been entered corresponding to one with letters on a phone keypad
            jump_index = self.letter_jump.get_index(KeyPress.numbers.index(key_code)) # get index to move to
            if jump_index is None:
                return
            self.position = jump_index // self.matrix_size.column  # find vertical scrolling position
            over_hang = self.position - self.max_position  # if at end of scroll
            rows_down = 0
            if over_hang > 0:  # set new position
                self.position = self.max_position
                rows_down = over_hang

            self.selected.set(ArrayPoint(jump_index % self.matrix_size.column, rows_down))  # set currently selected
            self.update_selected_colours(do_fade=False)  # update boarder position
            self.update_frames() # update frames
            self.arrows.change_colour(self.position, self.max_position)

            self.first_press.is_not()
        # up pressed and in top row
        elif key_code == KeyPress.up and self.selected.row == 0:
            if self.position > 0:  # if possible scroll up one
                self.position -= 1
                self.update_frames()
                self.arrows.change_colour(self.position, self.max_position)  # updates arrows colour

        # down and on bottom row
        elif key_code == KeyPress.down and self.selected.row + 1 == self.matrix_size.row:
            if self.can_scroll_down():  # if possible scroll down one
                self.position += 1
                self.update_frames()
                self.arrows.change_colour(self.position, self.max_position )  # updates arrows colour

                if self.position == self.max_position:  # check not an bottom row with no image inside
                    self.jump_to_frame(0, do_fade=False)

        else:  # change boarder position
            if not self.change_selected(key_code):  # if changed
                if self.selected.row < self.matrix_size.row - 1:  # jump if there is no image below
                    self.jump_to_frame(1)

    def jump_to_frame(self, rows_down, do_fade=True):
        """Jump to next available frame with image in it"""
        if self.tkinter_elements_matrix[self.selected.row + rows_down][self.selected.column].is_blank():  # if new position is blank
            for i in range(1, self.selected.column + 1):  # loop over frames in row
                if not self.tkinter_elements_matrix[self.selected.row + rows_down][self.selected.column - i].is_blank():  # if frame is not blank
                    self.selected.row += rows_down  # move position down
                    self.selected.column -= i  # set new column position
                    self.update_selected_colours(do_fade)
                    return

    def select_frame(self, i, j):
        """Select frame by row and column position"""

        self.first_press.is_not()

        self.selected_old.set(self.selected)  # set old selected

        self.selected = ArrayPoint(column=i, row=0)  # set new selected
        self.position = j  # set position down the grid

        difference = self.position - self.max_position  # if overhanging the end of the array

        if difference > 0:
            self.position -= difference  # take off the extra
            self.selected.row += difference  # and add to the row

        self.update_selected_colours(do_fade=False)  # update
        self.update_frames()
        self.arrows.reset_arrows(self.can_scroll_down())
        self.arrows.change_colour(self.position, self.max_position)

    def update_frames(self):
        """Updates the frame to the new scroll position"""
        for j in range(self.matrix_size.row):
            for i in range(self.matrix_size.column):
                self.tkinter_elements_matrix[j][i].update_text(self.frame_data[j + self.position][i])

    def get_location_index(self):
        """Get current position index"""
        return self.selected.column + (self.position + self.selected.row) * self.matrix_size.column

    def fade_borders(self):
        self.colours.fade_labels(old_label=self.tkinter_elements_matrix[self.selected_old.row][self.selected_old.column].label_image,
                                 new_label=self.tkinter_elements_matrix[self.selected.row][self.selected.column].label_image)