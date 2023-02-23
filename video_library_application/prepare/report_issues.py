class ReportIssues:
    """Contains information about problems creating thumbnails and contains method to print them"""
    def __init__(self):
        """Sets up list to hold issues"""
        self.report = []

    def write_error(self, *arg):
        """Takes error in the form of multiple arguments, print them to screen and add them to report list"""
        for line in arg:
            self.report.append(line)
            print(line)

    def print_report(self):
        """Prints any errors which may have occurred"""
        print("    ")
        if len(self.report) == 0:
            print("---No issues to report---")
        else:
            print("---Report---")
            for line in self.report:
                print(line)