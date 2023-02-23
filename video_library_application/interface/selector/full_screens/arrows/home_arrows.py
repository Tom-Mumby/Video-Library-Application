from video_library_application.config.sizes.fixed_sizes import ImageSize
from video_library_application.config.colours import Colours
from .parent_arrows import Arrow


class ArrowAcross(Arrow):
    """Creates the arrows moving across the page for the home frame, inherits from standard arrows"""
    def __init__(self, frame):
        """Sets the dimensions and adds the two arrows"""
        super().__init__(frame)
        # define size of the canvas
        self.y_size = ImageSize.height
        self.x_size = int(self.y_size/6)
        # changes shape of shape
        block_fraction = 0.4

        # sets the polygon points
        self.arrow1 = self.make_arrow([self.x_size,0,   self.x_size,self.y_size,    int((1-block_fraction)*self.x_size),self.y_size,    0,int(self.y_size/2),   int((1-block_fraction)*self.x_size),0])
        self.arrow2 = self.make_arrow([0,0,   int(block_fraction*self.x_size),0,    self.x_size,int(self.y_size/2),    int(block_fraction*self.x_size),self.y_size,   0,self.y_size])

    def reset_arrows(self, position_along):
        """Sets arrows to the correct starting position"""
        if position_along == 0:
            self.arrow1.change_colour_polygon(Colours.background)
            self.arrow2.change_colour_polygon(Colours.background)
        else:
            self.arrow1.change_colour_polygon(Colours.background)
            self.arrow2.change_colour_polygon(Colours.border)