import pygtk
pygtk.require('2.0')
import gtk
from image import Image

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

