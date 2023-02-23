import threading
import time
from ...config.key_press import KeyPress
from .marquee import Marquee


class VideoControls:
    """Enables video controls: fast-forward, pause, rewind, and skip"""
    def __init__(self, player):

        self.subtitle_numbers = []  # contains the usable subtitle numbers

        # creates object to display marquee over video
        self.marquee = Marquee(player)

        # if video is playing or not
        self.bool_playing = False
        # position as a decimal between 0 and 1
        self.position = 0

        # length of video file in milliseconds
        self.length_ms = None

        # time in seconds to update still image on screen which displays current location in video when fast-forwarding
        self.stop_time = 0.5
        self.player = player

        # list of booleans that when are true the corresponding threads loop and terminate when they are set to false
        self.loop = []

        # fast-forward/rewind speeds
        self.skip_speed = 0

    def set_playing(self, bool_set):
        """sets playing variable"""
        self.bool_playing = bool_set

    def get_playing(self):
        """returns playing variable"""
        return self.bool_playing

    def toggle_pause(self, b_clear):
        """Toggles pause on video"""

        if b_clear:  # set fast-forward speed to zero and clear the boolean that controls the fast-forward threads
            self.skip_speed = 0
            self.loop.clear()

        if self.player.is_playing():  # update marquee displaying and pause video
            self.marquee.update_marquee("Pause")
            self.player.set_pause(True)
        else:
            # remove info displaying over video and play video
            self.marquee.set_marquee(False)
            self.player.set_pause(False)

    def keypress(self, key_code):
        """Handle keypress event from user including: pause, play, rewind/fast-forward and, stop"""

        # if back button is pressed
        if self.get_playing() is True and (key_code == KeyPress.back or key_code == KeyPress.home):
            # reset the length of the video
            self.length_ms = None
            # set the end position of the video
            self.position = self.player.get_position()
            # turn off info displaying over video, needed so doesn't appear when playing the next video
            self.marquee.set_marquee(False)
            # stop the video
            self.player.stop()
            # change the value of the playing variable to indicate play has stopped
            self.set_playing(False)
            if key_code == KeyPress.home:  # if home was pressed set to different variable so can distinguish
                return None
            return None
        elif self.get_playing() is False:
            return False

        # if the video is already being fast-forwarded or rewound set last element in boolean loop
        # list to false in order to terminate the thread
        if len(self.loop) != 0:
            if self.loop[-1]:
                self.loop[-1] = False

        # if this is the first time a key has been pressed when the video is playing
        if self.length_ms is None:
            # clear the subtitle info from the previous video
            self.subtitle_numbers.clear()
            # get the video subtitle info and append the corresponding subtitle number to list
            description = self.player.video_get_spu_description()
            for value in description:
                self.subtitle_numbers.append(value[0])

            # set length of video in milliseconds
            self.length_ms = self.player.get_length()

            # set up marquee and pass it the length of the video to display it
            self.marquee.initialise(self.length_ms)

        # if the keypress code corresponds to a number entered on keypad
        if key_code in KeyPress.numbers:
            # change the position according to number entered, eg 3 is 3/10 of the way through the video
            key_number = KeyPress.numbers.index(key_code)
            if key_number == 9:  # if nine is pressed
                fraction = 0.96  # so jumps to 1 on exit
            else:
                fraction = key_number / 10

            self.player.set_position(fraction)

            # if player is paused set marquee to display it as such in case video is paused whilst being rewound
            if not self.player.is_playing():
                self.marquee.update_marquee("Paused")

        # if subtitles button is pressed
        elif key_code == KeyPress.menu_or_subtitles:
            # get current subtitle number
            subtitle = self.player.video_get_spu()
            # get position of current subtitle number in array
            try:
                index = self.subtitle_numbers.index(subtitle)
            except ValueError:
                return True
            # get the next position of the subtitle number, resetting the first subtitle if the end of the array is reached
            index += 1
            if index == len(self.subtitle_numbers):
                index = 0
            # set the subtitles according to the position in the subtitle array
            self.player.video_set_spu(self.subtitle_numbers[index])
        elif key_code == KeyPress.enter:
            # toggle pause function
            self.toggle_pause(True)
        # if arrow button has been pressed
        else:
            self.seek(key_code)
        return True

    def get_position(self):
        """ returns 0, unless the video has been stopped then returns last position in video as a decimal"""
        return self.position

    def seek(self, key_code):
        """Handles keypress event if it is one of the arrow keys"""

        def make_loop():
            """Creates text to display on screen about fast-forward and starts thread to keep moving the video position"""

            # converts so does not display with decimal
            self.skip_speed = int(self.skip_speed)
            # pause playing video
            self.player.set_pause(True)

            # if skipping forward
            if self.skip_speed > 0:
                text = "Forward x" + str(self.skip_speed)
            # if skipping backward
            else:
                text = "Backwards x" + str(abs(self.skip_speed))
            # creates new thread to keep skipping the video
            skip_loop = threading.Thread(target=change_position, args=(text, self.skip_speed * 1000,),daemon=True)
            # starts thread
            skip_loop.start()

        def change_position(text, jump_time):
            """Method is started as new thread to keep the video skipping"""

            # append variable the controls if loops runs to list
            self.loop.append(True)
            # set the index of the control variable for this loop
            index = len(self.loop) - 1
            # set time to jump forward by according to the skip rate
            jump_time = int(jump_time / self.stop_time)

            try:
                # while control variable is set
                while self.loop[index]:
                    # time to set video to
                    new_time = self.player.get_time() + jump_time
                    # if time is before start of video or after it finishes, play video and clear the list of control varaibles
                    if new_time < 0 or new_time > self.length_ms:
                        self.toggle_pause(True)
                        break
                    # update on screen config
                    self.marquee.update_marquee(text)
                    # set video to update time
                    self.player.set_time(new_time)
                    # pause before updating video position again
                    time.sleep(self.stop_time)
            except IndexError:
                # if index no longer exists exit thread
                pass
        # if right key is pressed skip forwards more
        if key_code == KeyPress.right:
            # if no speed is set
            if self.skip_speed == 0:
                self.skip_speed = 2
            # if already skipping forwards
            elif self.skip_speed >= 2:
                self.skip_speed *= 2
            # if skipping backwards
            elif self.skip_speed <= -4:
                self.skip_speed /= 2
            # if rewinding on slowest speed
            elif self.skip_speed == -2:
                self.skip_speed = 2
            # create thread
            make_loop()
        # if left key is pressed skip backwards more
        if key_code == KeyPress.left:
            # if no speed is set
            if self.skip_speed == 0:
                self.skip_speed = -2
            # if already skipping backwards
            elif self.skip_speed <= -2:
                self.skip_speed *= 2
            # if skipping forwards
            elif self.skip_speed >= 4:
                self.skip_speed /= 2
            # if fast-forwarding at the lowest speed
            elif self.skip_speed == 2:
                self.skip_speed = -2
            # create thread
            make_loop()

        # if up or down keys are pressed
        if key_code == KeyPress.up or key_code == KeyPress.down:
            # set time to move in milliseconds
            move_time = 12 * 1000
            # if down move time backwards
            if key_code == KeyPress.down:
                move_time *= -1
            # set the new time in milliseconds
            new_time = self.player.get_time() + move_time
            # if the new time is within the video play time set time
            if 0 < new_time < self.length_ms:
                self.player.set_time(new_time)
                # if video is paused update info displaying to new time
                if not self.player.is_playing():
                    self.marquee.update_marquee("Pause")