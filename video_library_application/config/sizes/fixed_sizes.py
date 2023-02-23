"""Contains various constants for the GUI that define the fixed sizes for elements within the GUI"""

from video_library_application.array_point import ArrayPoint

# Sets the dimensions of the main grid within the GUI
MainGridDimensions = ArrayPoint(column=3, row=2)


class ScreenSize:
    """Sets the size of a HD screen and the aspect ratio"""
    height = 1080
    width = 1920
    aspect_ratio = width / height  # screen aspect ratio


class ImageSize:
    """Sets the size of an image within the GUI"""
    image_y_fraction = 0.5  # fraction of the total height of the screen the images should occupy
    height = int(round(ScreenSize.height * image_y_fraction / MainGridDimensions.row))  # image height
    width = int(round(height * ScreenSize.aspect_ratio))  # image width
    boarder_width = height / 15  # fraction of the image height the boarder takes up


class MenuSize:
    """Sets the size of the menu within the GUI"""
    menu_x_fraction = 0.3  # fraction of the screen width the menu should occupy
    icon_y_fraction = 0.1  # fraction of the screen height the menu icon should occupy
    width = int(round(ScreenSize.width * menu_x_fraction))  # menu width
    icon_padding_size = round(ScreenSize.height * icon_y_fraction / 7)
    icon_size = icon_padding_size * 7
    progress_height = icon_size // 4  # height of the progress bar within the menu (when scanning for new files)



