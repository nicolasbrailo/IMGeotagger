import pygtk
pygtk.require('2.0')
import gtk
from embedded_browser import create_embedded_browser
from img_list import Img_List

class Wnd(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)

        self.connect('destroy', self.on_exit)
        self.set_size_request(width=800, height=600)
        self.set_title('IMGeotagger')
        self.realize()

        self.btn = gtk.Button("Click me")
        self.btn.connect('button-press-event', self.btn1)

        self.img_list = Img_List("/home/laptus/Pictures/Fotos/00to_tag/nexus_save/")
        self.img_list.get_selection().connect("changed", self.on_image_selection)

        img_select_layout = gtk.VBox(False, 0)
        vscroll = gtk.ScrolledWindow()
        vscroll.set_policy(hscrollbar_policy=gtk.POLICY_NEVER, vscrollbar_policy=gtk.POLICY_AUTOMATIC)
        vscroll.add_with_viewport(self.img_list)

        img_select_layout.pack_start(vscroll, True, True, 0)
        img_select_layout.pack_start(self.btn, False, False, 0)

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
        print "HOLA"

w = Wnd()
gtk.main()

