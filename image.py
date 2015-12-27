import pyexiv2

class Image(object):
    def __init__(self, fullpath, fname):
        self._fullpath = fullpath
        self._fname = fname

        self._metadata = pyexiv2.ImageMetadata(self._fullpath)
        self._metadata.read()

    def get_fullpath(self):
        return self._fullpath

    def get_fname(self):
        return self._fname

    def get_date(self):
        try:
            return self._metadata['Exif.Photo.DateTimeOriginal'].value.strftime('%d %B %Y, %H:%M:%S')
        except KeyError:
            return ''

    def get_position(self):
        try:
            lat_key_ref = 'Exif.GPSInfo.GPSLatitudeRef' # S/N
            lat_key = 'Exif.GPSInfo.GPSLatitude'
            lat = str(self._sex_to_dec(self._metadata[lat_key].value)) + self._metadata[lat_key_ref].raw_value

            lon_key_ref = 'Exif.GPSInfo.GPSLongitudeRef' # West/East
            lon_key = 'Exif.GPSInfo.GPSLongitude'
            lon = str(self._sex_to_dec(self._metadata[lon_key].value)) + self._metadata[lon_key_ref].raw_value
        except KeyError:
            return 'Not set'

        return lat + ' ' + lon

    def set_position(self, coords):
        print 'Setting {} to {}'.format(self._fullpath, coords)

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
