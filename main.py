import pygtk
pygtk.require('2.0')
import gtk
from embedded_browser import create_embedded_browser
from img_list import Img_List
from image_control import Image_Control

class Wnd(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)

        self.connect('destroy', self.on_exit)
        self.set_size_request(width=800, height=600)
        self.set_title('IMGeotagger')
        self.realize()

        self.img_list = Img_List('/home/laptus/Pictures/Fotos/00to_tag/nexus_save/')
        self.img_list.get_selection().connect('changed', self.on_image_selection)

        self.img_ctrl = Image_Control(self.callback_set_gps_pos_requested,
                                      self.callback_open_new_path)

        img_select_layout = gtk.VBox(False, 0)
        img_select_layout.pack_start(self.img_ctrl, False, False, 2)
        img_select_layout.pack_start(self.img_list.get_ui_element(), True, True, 0)

        self.layout = gtk.HBox(False, 5)
        self.layout.pack_start(img_select_layout, False, False, 0)
        self.add(self.layout)
        self.browser = create_embedded_browser(self.layout,
                                    #'http://example.net')
                                    'https://www.google.nl/maps/@37.2870888,22.3544721,4.33z')

        self.show_all()

    def on_exit(self, widget, data=None):
        gtk.main_quit()

    def callback_open_new_path(self, path):
        self.img_list.set_path(path)

    def callback_set_gps_pos_requested(self):
        coords = Wnd.hack_coords_from_gmaps(self.browser.get_url())
        for img in self.img_list.get_current_selection():
            img.set_position(coords)

    def on_image_selection(self, widget, data=None):
        self.img_ctrl.on_images_selected(self.img_list.get_current_selection())

    @staticmethod
    def hack_coords_from_gmaps(map_path):
        """ Tries to get the map coords from the url of a Google maps page """
        #Expected URL format: https://www.google.nl/maps/@37.2870888,22.3544721,4z
        start_tok = 'https://www.google.nl/maps/@'
        lat_pos = map_path.find(start_tok) + len(start_tok)
        lat_end = map_path.find(',', lat_pos)
        lon_pos = lat_end + 1
        lon_end = map_path.find(',', lon_pos)
        
        if (lat_pos < 0) or (lat_end < 0) or (lon_pos < 0) or (lon_end < 0):
            print "Fatal error: the URL format for Google maps has changed and " + \
                  "this program can't understand it. Unknown URL: {0}".format(map_path)
            exit(1)

        return (float(map_path[lat_pos:lat_end]), float(map_path[lon_pos:lon_end]))


w = Wnd()
gtk.main()

