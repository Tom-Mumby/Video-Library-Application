import vlc


class Marquee:
    """Creates textual marquee to display over video when paused"""
    def __init__(self, player):
        self.player = player

    @staticmethod
    def time_string(time_ms):
        """Takes time in milliseconds and returns a readable string to display over video"""

        # converts time to seconds
        time = int(time_ms / 1000)
        # initilise string to contain time
        s_time = ""
        # if longer than an hour
        if time > 3600:
            # add number of hours to string
            s_time = s_time + str(time // 3600) + ":"
            # remove the contribution from the hours from the time in seconds
            time = time % 3600
            # if less then one minute add zero to display string
            if time // 60 < 10:
                s_time = s_time + "0"
        # add number of minutes to display string
        s_time = s_time + str(time // 60) + ":"

        # the contribution from the minutes from the time in seconds
        time = time % 60
        # if less then 10 seconds add zero to display string
        if time % 60 < 10:
            s_time = s_time + "0"

        # add time in seconds to display string
        s_time = s_time + str(time)

        # return display string
        return s_time

    def initialise(self, length):
        """Sets up the needed parts for the info to be displayed over the video for each new one"""

        # creates display time string for the total length of the video
        self.length_string = self.time_string(length)

        # get the height of the text to display as a fraction of the total video height
        text_height = int(self.player.video_get_height() * 0.08)
        # get the padding for the distance from the top and left of the video
        padding = int(text_height/4)
        # set padding amounts
        self.player.video_set_marquee_int(vlc.VideoMarqueeOption.X, padding)
        self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Y, padding)
        # set the text size
        self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Size, text_height)

    def update_marquee(self, state):
        """Updates the text in the marquee when the video is paused or rewound"""

        # turns marquee on
        self.set_marquee(True)
        # get the current time in video as a readable string
        s_marquee = self.time_string(self.player.get_time())
        # creates string to display in marquee, combining the state of the video i.e. paused, forwards, backwards, the current time and the total time
        s_marquee = state + " - " + s_marquee + " / " + self.length_string
        # updates text in marquee
        self.player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, s_marquee)

    def set_marquee(self, b_set):
        """Turns marquee on or off"""
        self.player.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, b_set)