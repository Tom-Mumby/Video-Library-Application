from video_library_application.config.sizes.fixed_sizes import ImageSize
from video_library_application.config.colours import Colours
from .make_text_image import TextImage

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw


class SubFrameImage(tk.Frame):
    """tkinter image frame, contains methods to set image within frame and update"""
    def __init__(self, parent, frame_data):
        """Creates the image within the frame"""
        tk.Frame.__init__(self, parent)
        self.config(bg=Colours.background)  # set background colour

        self.frame_data = frame_data  # set the initial frame data
        self.tk_image = ImageTk.PhotoImage(self.get_image()) # included or image gets garbage collected
        # make tk-label containing image
        self.label_image = tk.Label(self, image=self.tk_image, borderwidth=ImageSize.boarder_width, bg=Colours.background)
        self.label_image.pack()

    def get_image(self):
        """gets the correct type of image to assign to the label"""

        def do_thumbnail_load(path):
            """returns thumbnail file, checking if it needs resizing"""
            try:  # getting image saved in file
                # open image
                img = Image.open(path)

                if img.size[0] == ImageSize.width and img.size[1] == ImageSize.height: # correct size
                    return img
                else:
                    img = img.resize((ImageSize.width, ImageSize.height)) # resize image to correct size
                    return img

            except IOError:  # if fails make a text image
                return TextImage.make_text_image(self.frame_data.name)

        def add_progress_bar(img, progress):
            width, height = img.size # finds the size of the image

            fill_colour = Colours.progress  # block colour of bar
            tint_colour = (0, 0, 0, int(255 * 0.5))  # set tint colour where bar is over image to black and opacity
            img = img.convert("RGBA")  # convert so can apply composite

            block_height = height - ImageSize.boarder_width  # height to make the progress bar
            block_width = int(width * progress)  # width to make the progress bar

            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))  # create blank image to overlay
            draw = ImageDraw.Draw(overlay)  # create a context for drawing things on it
            draw.rectangle(((block_width, block_height), (width, height)), fill=tint_colour)  #  created tinted area over image

            img = Image.alpha_composite(img, overlay)  # merge the two images together
            img = img.convert("RGB") # remove alpha for saving in jpg format
            draw = ImageDraw.Draw(img)  # set so can draw on image
            draw.rectangle(((0, block_height), (block_width, height)), fill=fill_colour)  # draw filled rectangle

            # return image with progress bar overlayed
            return img

        if type(self.frame_data).__name__ == "BlankData":
            image = Image.new('RGB', (ImageSize.width, ImageSize.height), color=Colours.background)
        elif type(self.frame_data).__name__ == "PlacardData":
            image = TextImage.make_text_image(self.frame_data.name)
        else:
            image = do_thumbnail_load(self.frame_data.thumbnail_path)
            if self.frame_data.progress is not None:
                image = add_progress_bar(image, self.frame_data.progress)

        self.frame_data.set_image(image)  # set image to frame data
        return image

    def update_image(self, frame_data):
        """Updates the current image"""
        self.frame_data = frame_data  # sets the new frame data
        if self.frame_data.image is None:  # if image hasn't been made yet
            self.tk_image = ImageTk.PhotoImage(self.get_image())  # make new image
        else:  # image has been made
            self.tk_image = ImageTk.PhotoImage(frame_data.image)  # set image to tkinter label

        self.label_image.configure(image=self.tk_image)  # update image in label

    def get_information(self):
        return self.frame_data

    def is_blank(self):
        """returns true if frame is blank"""
        if type(self.frame_data).__name__ == "BlankData":
            return True
        else:
            return False
