import tkinter as tk


class CanvasPolygon(tk.Canvas):
    """Extends the tkinter canvas class to allow polygons to be added to the canvas and the colours to be changed"""

    def __init__(self, parent, x_size, y_size, colour):
        """Sets up the canvas and initialises an array to contain the polygons"""
        tk.Canvas.__init__(self, parent)
        self.config(bg=colour, height=y_size, width=x_size, highlightthickness=0)
        self.drawn_shapes = []

    def add_polygon(self, points, colour):
        """Adds a polygon to the canvas"""
        self.drawn_shapes.append(self.create_polygon(points, fill=colour))

    def add_to_grid(self, row, col, padding_x=0, padding_y=0, col_span=1):
        """Adds the canvas to a tkinter frame using the grid layout"""
        self.grid(row=row, column=col, pady=padding_y, padx=padding_x, columnspan=col_span, sticky=tk.E)

    def add_to_frame(self):
        """Adds the canvas to a tkinter frame using the packing layout"""
        self.pack()

    def remove_polygons(self):
        """Removes all the polygons from the canvas"""
        for shape in self.drawn_shapes:
            self.delete(shape)

    def change_colour_polygon(self, colour):
        """Changes to colour of all of the polygons"""
        for i in range(len(self.drawn_shapes)):
            self.itemconfig(self.drawn_shapes[i], fill=colour)
        self.update()

    def change_colour_canvas(self, colour):
        """Changes the colour of the canvas, i.e. the background colour"""
        self.config(bg=colour)
