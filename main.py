import pygtk
pygtk.require('2.0')
import gtk
from embedded_browser import create_embedded_browser
from img_list import Img_List

class Image_Control(gtk.VBox):
    def __init__(self, on_set_position_called):
        gtk.VBox.__init__(self, False, 0)

        self.lbl_img_info = gtk.Label()
        self.lbl_img_info.set_use_markup(gtk.TRUE)

        self.btn_set_pos = gtk.Button("Set position")
        self.btn_set_pos.connect('button-press-event', on_set_position_called)

        self.pack_start(self.lbl_img_info, False, False, 2)
        self.pack_start(self.btn_set_pos, False, False, 2)

        self.on_selection_cleared()

    def on_images_selected(self, img_list):
        if len(img_list) == 0:
            self.on_selection_cleared()
            return
        elif (len(img_list) == 1):
            self.lbl_img_info.set_markup("<b>Filename: " + img_list[0].get_fname() + "\n" + \
                                            "Date:     " + img_list[0].get_date() + "\n" + \
                                            "Position: " + img_list[0].get_position() + "</b>")
        else:
            self.lbl_img_info.set_markup("<b>Filename: Multiple\n" + \
                                            "Date:     ---\n" + \
                                            "Position: ---</b>")

        self.btn_set_pos.set_sensitive(True)

    def on_selection_cleared(self):
        self.btn_set_pos.set_sensitive(False)
        self.lbl_img_info.set_markup("<b>Filename: ---\n" + \
                                        "Date:     ---\n" + \
                                        "Position: ---</b>")

class Wnd(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self)

        self.connect('destroy', self.on_exit)
        self.set_size_request(width=800, height=600)
        self.set_title('IMGeotagger')
        self.realize()

        self.img_list = Img_List("/home/laptus/Pictures/Fotos/00to_tag/nexus_save/")
        self.img_list.get_selection().connect("changed", self.on_image_selection)

        self.img_ctrl = Image_Control(self.btn1)

        img_select_layout = gtk.VBox(False, 0)
        img_select_layout.pack_start(self.img_ctrl, False, False, 2)
        img_select_layout.pack_start(self.img_list.get_ui_element(), True, True, 0)

        self.layout = gtk.HBox(False, 5)
        self.layout.pack_start(img_select_layout, False, False, 0)
        self.add(self.layout)
        self.browser = create_embedded_browser(self.layout,
                                    'http://example.net')
                                    #'https://www.google.nl/maps/@37.2870888,22.3544721,4.33z')

        self.show_all()

    def on_exit(self, widget, data=None):
        gtk.main_quit()

    def btn1(self, widget, data=None):
        print self.browser.get_url()

    def on_image_selection(self, widget, data=None):
        self.img_ctrl.on_images_selected(self.img_list.get_current_selection())

w = Wnd()
gtk.main()

