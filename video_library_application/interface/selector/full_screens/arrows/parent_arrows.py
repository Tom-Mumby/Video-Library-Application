from video_library_application.config.colours import Colours
from ...canvas_polygon import CanvasPolygon
from ...change_label_colour import ChangeLabelColour


class Arrow:
    """Creates and acts on the arrows which indicate how many more items there are in the home or selection frames"""

    def __init__(self, frame):
        """Sets the parent frame"""
        self.frame = frame
        self.colours = ChangeLabelColour(default_colour=Colours.background, selected_colour=Colours.border)

    def make_arrow(self, points):
        """makes a arrow and puts it in the grid"""
        arrow = CanvasPolygon(self.frame, x_size=self.x_size, y_size=self.y_size, colour=Colours.background)
        arrow.add_polygon(points, colour=Colours.border)
        return arrow

    def change_colour(self, curr_position, max_position):
        """Changes colour of the arrows to indicates how for through the scrollable distance"""
        # if not enough items to scroll
        if max_position == 0:
            return

        # fraction of total scroll
        fraction = curr_position / max_position

        # change arrow colour and update
        self.arrow1.change_colour_polygon(self.colours.get_mixture(fraction))
        self.arrow2.change_colour_polygon(self.colours.get_mixture(1-fraction))

