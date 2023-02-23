class BlankData:
    """Contains data to make a blank sub-frame"""
    def __init__(self):
        self.name = "    "
        self.progress = None
        self.image = None

    def set_image(self, image):
        self.image = image

    def get_name(self):
        return self.name