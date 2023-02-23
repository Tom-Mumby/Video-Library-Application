class ReadTextFile:
    """Reads a text file from disk and returns text"""
    @staticmethod
    def do_read(path):
        # open file containing the key code and read content
        f = open(path, "r", encoding="utf-8")
        content = f.read()
        content = content.splitlines()
        f.close()
        return content
