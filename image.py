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
        lat_key_ref = 'Exif.GPSInfo.GPSLatitudeRef' # S/N
        lat_key = 'Exif.GPSInfo.GPSLatitude'
        lat = str(self._sex_to_dec(self._metadata[lat_key].value)) + self._metadata[lat_key_ref].raw_value

        lon_key_ref = 'Exif.GPSInfo.GPSLongitudeRef' # West/East
        lon_key = 'Exif.GPSInfo.GPSLongitude'
        lon = str(self._sex_to_dec(self._metadata[lon_key].value)) + self._metadata[lon_key_ref].raw_value

        return lat + ' ' + lon

    def _dec_to_sex(self, x):
        degrees = int(math.floor(x))
        minutes = int(math.floor(60 * (x - degrees)))
        seconds = int(math.floor(6000 * (60 * (x - degrees) - minutes)))
        return (pyexiv2.utils.make_fraction(degrees, 1), pyexiv2.utils.make_fraction(minutes, 1), pyexiv2.utils.make_fraction(seconds, 100))

    def _sex_to_dec(self, fractions):
        degrees = float(fractions[0])
        minutes = float(fractions[1])
        seconds = float(fractions[2])    
        minutes = minutes + (seconds/60)
        degrees = degrees + (minutes/60)
        return degrees
