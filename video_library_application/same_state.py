class SameState:
    """Checks if a variable has been changed from the starting state"""
    def __init__(self):
        """Sets start state to true"""
        self.reset()

    def reset(self):
        """Resets state to true"""
        self.same_state = True

    def is_not(self):
        """Checks if state is no longers true"""
        if self.same_state is True:
            self.same_state = False

    def is_still(self):
        """Checks if state is still ture"""
        return self.same_state

