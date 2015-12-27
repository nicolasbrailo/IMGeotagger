import pyexiv2

class Image(object):
    def __init__(self, fullpath, fname):
        self.fullpath = fullpath
        self.fname = fname

        self._metadata = pyexiv2.ImageMetadata(self.fullpath)
        self._metadata.read()

    def get_fullpath(self):
        return self.fullpath

    def get_fname(self):
        return self.fname

    def get_date(self):
        key = "Exif.Photo.DateTimeOriginal"
        try:
            return self._metadata[key].value.strftime('%d %B %Y, %H:%M:%S')
        except KeyError:
            return ""
        except Exception, e:
            print ("can not get date/time '%s' for image '%s': %s" % (self._metadata[key].raw_value, self.path_full, str(e)))

    def get_position(self):
        return "41.1234 / 12.1234"

