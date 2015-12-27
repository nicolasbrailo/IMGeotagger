
class Image(object):
    def __init__(self, fullpath, fname):
        self.fullpath = fullpath
        self.fname = fname

    def get_fullpath(self):
        return self.fullpath

    def get_fname(self):
        return self.fname

    def get_date(self):
        return "0/0/0"

    def get_position(self):
        return "41.1234 / 12.1234"

