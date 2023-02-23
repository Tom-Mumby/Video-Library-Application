from video_library_application.config.sizes.fixed_sizes import ImageSize, ScreenSize


class RelativeSizes:
    """Returns screen sizes as a fraction of the total screen height or a fraction of the standard test size"""
    text_y_fraction = 0.1  # fraction of the screen height standard text unit takes up
    text_size = ImageSize.height * text_y_fraction  # sets standard text size

    @staticmethod
    def get_height_percent(scale):
        """Get percent of the screen height and scale"""
        return int(scale * ScreenSize.height / 100)

    @classmethod
    def get_text_size(cls, scale):
        """Get text size and scale"""
        return int(cls.text_size * scale)