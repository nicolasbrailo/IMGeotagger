import pygtk
pygtk.require('2.0')
import gtk
from embedded_browser import create_embedded_browser

class Wnd(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)

        self.connect('destroy', self.on_exit)
        self.set_size_request(width=800, height=600)
        self.set_title('Tagtag')
        self.realize()

        self.btn = gtk.Button("Click me")

        self.btn.connect('button-press-event', self.btn1)

        self.layout = gtk.HBox(False, 0)
        self.layout.pack_start(self.btn, False, False, 0)
        self.add(self.layout)
        self.browser = create_embedded_browser(self.layout,
                                    'https://www.google.nl/maps/@37.2870888,22.3544721,4.33z')

        self.show_all()

    def on_exit(self, widget, data=None):
        gtk.main_quit()

    def btn1(self, widget, data=None):
        print self.browser.get_url()
        gc = self.get_style().fg_gc[gtk.STATE_NORMAL]
        self.window.draw_line(gc, 0, 0, 200, 200)
        self.btn.window.draw_line(gc, 0, 0, 200, 200)


w = Wnd()
gtk.main()

