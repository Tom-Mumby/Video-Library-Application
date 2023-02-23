from video_library_application.config.sizes.fixed_sizes import MenuSize
from video_library_application.config.colours import Colours
from video_library_application.interface.selector.canvas_polygon import CanvasPolygon
import tkinter as tk


class MenuIconFrame(tk.Frame):
    """Creates the menu icon which appears in the full-screen home frame and the selection frames at all times"""

    # sets the size to make the icon and the padding around it
    padding_size = MenuSize.icon_padding_size
    canvas_size = MenuSize.icon_size

    # sets the colours to make the icon
    bar_colour = Colours.text
    canvas_colour = Colours.box

    def __init__(self, parent):
        """Creates the icon and adds it to the frame"""
        tk.Frame.__init__(self, parent)

        def add_menu_bars():
            """Adds each of the three bars to the icon, changing the position of the bar it is adding each time"""
            for j in range(3):
                self.icon.add_polygon(box_points, self.bar_colour)
                for i in range(len(box_points)):
                    if i % 2 != 0:  # if odd
                        box_points[i] = box_points[i] + 2 * self.padding_size

        # sets position of the first menu bar
        box_points = [self.padding_size,self.padding_size, self.canvas_size-self.padding_size,self.padding_size, self.canvas_size-self.padding_size,self.padding_size * 2, self.padding_size,self.padding_size * 2]

        # initialises the icon
        self.icon = CanvasPolygon(parent=self, x_size=self.canvas_size, y_size=self.canvas_size, colour=self.canvas_colour)
        add_menu_bars()
        self.icon.add_to_frame()

    def highlight(self):
        """Changes the colours with the affect of highlighting the canvas"""
        self.icon.change_colour_polygon(self.canvas_colour)
        self.icon.change_colour_canvas(self.bar_colour)

    def lowlight(self):
        """Changes the colours with the affect of returning the canvas to its original colours"""
        self.icon.change_colour_polygon(self.bar_colour)
        self.icon.change_colour_canvas(self.canvas_colour)