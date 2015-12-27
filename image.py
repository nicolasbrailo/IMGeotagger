
class Image(object):
    def __init__(self, fullpath, fname):
        self.fullpath = fullpath
        self.fname = fname

    def get_fullpath(self):
        return self.fullpath

    def get_fname(self):
        return self.fname
