class KeyPress:
    """Sets the keycodes from keysym for tkinter Keypress event"""

    left = "Left"
    right = "Right"
    up = "Up"
    down = "Down"
    enter = "Return"
    back = "BackSpace"
    menu_or_subtitles = "m"
    home = "h"

    numbers = []
    for i in range(10):
        numbers.append(str(i))