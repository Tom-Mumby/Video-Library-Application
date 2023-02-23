import sys


class SystemType:
    """Sets the folder separator for the type of operating system"""
    isWindows = sys.platform.startswith('win')
    isLinux   = sys.platform.startswith('linux')
    # sets folder separator for system
    if isWindows:
        folder_sep = "\\"
    if isLinux:
        folder_sep = "/"
