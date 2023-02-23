class ChangeLabelColour:
    """Contains methods to convert between HEX and RGB colours and to change the colour of tkinter elements"""

    number_fades = 6  # number of border fades; should be even
    time_ms = 150  # time to fade
    pause_time = int(time_ms / number_fades)  # time for each colour change

    def __init__(self, default_colour, selected_colour):
        """Sets the two colours in HEX and RGB, creates a step colour to change between them"""

        self.hex_default_colour = default_colour
        self.hex_selected_colour = selected_colour

        self.rgb_default_colour = self._to_rgb(self.hex_default_colour)
        self.rgb_selected_colour = self._to_rgb(self.hex_selected_colour)

        self.step_to_default = []
        for i in range(3):  # amount to add to rgb colour for each fade, going towards the default colour
            self.step_to_default.append(round((self.rgb_default_colour[i] - self.rgb_selected_colour[i]) / self.number_fades))

    def get_mixture(self, fraction):
        """returns a fraction between two colours"""
        colour_mixture = [0] * 3
        # makes the correct colour based on fraction
        for i in range(3):
            colour_mixture[i] = round((self.rgb_selected_colour[i] - self.rgb_default_colour[i]) * fraction + self.rgb_default_colour[i])
        # converts it to hex
        hex_mixture = self._to_hex(colour_mixture)

        return hex_mixture

    def set_default(self, label):
        """sets to default colour"""
        label = self._check_for_label(label)
        label.config(background=self.hex_default_colour)

    def set_selected(self, label):
        """sets to selected (highlighted colour"""
        label = self._check_for_label(label)
        label.config(background=self.hex_selected_colour)

    def fade_labels(self, old_label, new_label):
        """fades between the colours for two given labels"""
        old_label = self._check_for_label(old_label)
        new_label = self._check_for_label(new_label)

        colour_old = [0] * 3
        colour_new = [0] * 3
        # loop over number of fades
        for i in range(1, self.number_fades+1):
            # get new colours
            for j in range(3):
                colour_old[j] = self.rgb_selected_colour[j] + (self.step_to_default[j] * i * 1)
                colour_new[j] = self.rgb_default_colour[j] + (self.step_to_default[j] * i * -1)
            # convert to HEX
            hex_old = self._to_hex(colour_old)
            hex_new = self._to_hex(colour_new)
            # sleep to delay fade
            old_label.after(self.pause_time)
            # configure new colours
            old_label.config(background=hex_old)
            new_label.config(background=hex_new)
            # update labels
            old_label.update()
            new_label.update()
        # set new colours at end to ensure correct colours
        old_label.config(background=self.hex_default_colour)
        new_label.config(background=self.hex_selected_colour)

    @staticmethod
    def _check_for_label(label):
        """if a frame has been passed get label from it"""
        try:
            return label.label_image
        except AttributeError:
            return label

    @staticmethod
    def _to_rgb(hex_colour):
        """Takes a HEX colour and converts it to RGB"""
        rgb = []
        for i in (1, 3, 5):
            decimal = int(hex_colour[i:i+2], 16)
            rgb.append(decimal)
        return rgb

    @staticmethod
    def _to_hex(rgb_colour):
        """Takes an RGB colour and converts it to a HEX"""
        hex_string = "#"
        for i in range(3):
            if rgb_colour[i] < 0:
                rgb_colour[i] = 0
            element = str('{:x}').format(rgb_colour[i])
            if len(element) == 1:
                hex_string = hex_string + "0"
            hex_string = hex_string + element
        return hex_string
