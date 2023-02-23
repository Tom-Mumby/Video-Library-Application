from video_library_application.config.sizes.fixed_sizes import ImageSize
from video_library_application.config.colours import Colours
from .parent_arrows import Arrow


class ArrowUpDown(Arrow):
    """Creates the up/down arrows for the selection frame, inherits from the standard arrows class"""

    def __init__(self, frame):
        """Sets the dimensions and adds the two arrows"""
        super().__init__(frame)
        # define size of the canvas
        self.y_size = int(ImageSize.height / 15)
        self.x_size = ImageSize.width * 2
        # changes shape of shape
        block_fraction = 0.01
        # sets the polygon points
        self.arrow1 = self.make_arrow([0,self.y_size, int(block_fraction*self.x_size),0, int(self.x_size * (1 - block_fraction)),0, self.x_size,self.y_size])
        self.arrow2 = self.make_arrow([0,0, int(block_fraction*self.x_size),self.y_size, int(self.x_size * (1 - block_fraction)),self.y_size, self.x_size,0])

    def reset_arrows(self, can_scroll_down):
        """Sets arrows to the starting position"""
        if can_scroll_down:  # can go down
            self.arrow1.change_colour_polygon(Colours.background)
            self.arrow2.change_colour_polygon(Colours.border)
        else:
            self.arrow1.change_colour_polygon(Colours.background)
            self.arrow2.change_colour_polygon(Colours.background)

