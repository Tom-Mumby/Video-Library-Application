from video_library_application.config.key_press import KeyPress
from video_library_application.array_point import ArrayPoint
from ...position import Position


class SlidePosition(Position):
    """Handles changing boarders on the frames within the home frame and changing which sub-frames are displayed"""

    def __init__(self, frames, frame_data, arrows_top, arrows_bottom, default_colour, selected_colour):
        """Adds the two sets of arrows and sets the positions of the top and bottom rows"""
        super().__init__(frames, default_colour, selected_colour)
        self.frame_data = frame_data  # set the data within the frames
        self.arrows_top = arrows_top
        self.arrows_bottom = arrows_bottom
        self.top_position = 0  # position along in the top row
        self.bottom_position = 0  # position along in the bottom row
        self.max_top = len(frame_data[0]) - self.matrix_size.column  # set the maximum number of steps to move along on the top row
        if self.max_top < 0:
            self.max_top = 0

        self.max_bottom = 0
        self.set_max_bottom()

        self.arrows_top.reset_arrows(self.max_top)  # reset arrows along the top
        self.arrows_bottom.reset_arrows(self.max_bottom)  # reset arrows along the bottom

    def set_max_bottom(self):
        """Sets the maximum number of steps to move along on the bottom row"""
        self.max_bottom = len(self.frame_data[1]) - self.matrix_size.column
        if self.max_bottom < 0:
            self.max_bottom = 0

    def change_position(self, key_code):
        """Changes the slide position of the top and bottom rows"""
        # = event.keycode  # get the keycode
        if key_code not in [KeyPress.up, KeyPress.left, KeyPress.right, KeyPress.down]:
            return  # not an arrow key

        self.selected_old.set(self.selected)

        # left key pressed and in top row
        if key_code == KeyPress.left and self.selected.row == 0:
            if self.selected.column == 0 and self.top_position > 0:  # in leftmost position and able to shift
                self.top_position -= 1  # move position
                self.update_frames_top()  # update the frames
                self.arrows_top.change_colour(self.top_position, self.max_top)

        # right key pressed and in top row
        elif key_code == KeyPress.right and self.selected.row == 0:
            if self.selected.column == (self.matrix_size.column - 1) and self.top_position < self.max_top:  # in rightmost position and can shift
                self.top_position += 1  # move position
                self.update_frames_top()  # update frames
                self.arrows_top.change_colour(self.top_position, self.max_top)

        # left key pressed and in bottom row
        elif key_code == KeyPress.left and self.selected.row == 1:
            if self.selected.column == 0 and self.bottom_position > 0:  # in leftmost position and able to shift
                self.bottom_position -= 1  # move position
                self.update_frames_bottom()  # update frames
                self.arrows_bottom.change_colour(self.bottom_position, self.max_bottom)

        # right key pressed and in bottom row
        elif key_code == KeyPress.right and self.selected.row == 1:
            if self.selected.column == (self.matrix_size.column - 1) and self.bottom_position < self.max_bottom:# in rightmost position and can shift
                self.bottom_position += 1  # move position
                self.update_frames_bottom()  # update frames
                self.arrows_bottom.change_colour(self.bottom_position, self.max_bottom)

        self.change_selected(key_code)  # change boarder

    def reset_after_watched(self, reset_border=True):
        """Resets the position of the bottom row after a video has been watched"""
        self.set_max_bottom()
        self.bottom_position = 0  # reset watched videos to start
        if reset_border:
            # sets the selected frame to be the bottom left
            self.selected_old.set(self.selected)
            self.selected.set(ArrayPoint(0,1))
            self.update_selected_colours(do_fade=False)

        # updates the frames
        self.arrows_bottom.reset_arrows(self.max_bottom)
        self.update_frames_bottom()

    def update_frames_top(self):
        """updates the frames for the new position"""
        for i in range(self.matrix_size.column):  # loop over both rows
            self.tkinter_elements_matrix[0][i].update_image(self.frame_data[0][i+self.top_position])  # for each frame in top row, pass the new frame data

    def update_frames_bottom(self):
        """updates the frames for the new position"""
        for i in range(self.matrix_size.column):  # loop over both rows
            self.tkinter_elements_matrix[1][i].update_text(self.frame_data[1][i+self.bottom_position])  # for each frame in bottom row, pass the new frame data

    def get_location_index(self):
        """returns the position of the selected frame"""
        if self.selected.row == 0:  # on top row
            return 0, self.top_position + self.selected.column
        if self.selected.row == 1:  # on bottom row
            return 1, self.bottom_position + self.selected.column