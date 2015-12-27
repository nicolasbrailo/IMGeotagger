import gtk
import glib
import os
import gobject
from image import Image

class Img_List(gtk.TreeView):
    """ List of images in a path """

    def __init__(self, start_path):
        self.elements = gtk.ListStore(Img_List.UI_Image, gtk.gdk.Pixbuf, str)
        gtk.TreeView.__init__(self, self.elements)

        self.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

        #cell renderers for image and image name
        column_pixbuf = gtk.TreeViewColumn("Image", gtk.CellRendererPixbuf(), pixbuf=1)
        self.append_column(column_pixbuf)
        column_text = gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=2)
        self.append_column(column_text)

        # Provide a nice scrollable window for the users convenience but still extend
        # a TreeView: most of the functionality a caller would need is in there, so
        # making this class extend a ScrolledWindow would require a lot of scaffolding
        self.vscroll = gtk.ScrolledWindow()
        self.vscroll.set_policy(hscrollbar_policy=gtk.POLICY_NEVER, vscrollbar_policy=gtk.POLICY_AUTOMATIC)
        self.vscroll.add_with_viewport(self)

        self.set_path(start_path)

    def get_ui_element(self):
        return self.vscroll

    def get_current_selection(self):
        (model, selection) = self.get_selection().get_selected_rows()
        return [model.get_value(model.get_iter(i), 0).as_image() for i in selection]

    def set_path(self, path):
        self.elements.clear()
        if not os.path.isdir(path): return

        lst = os.listdir(path)
        lst.sort()
        images = list()
        for filename in lst:
            if filename.upper().endswith("JPG") or filename.upper().endswith("PNG"):
                images.append(os.path.join(path, filename))

        loader = self._load_elements(images)
        glib.idle_add(loader.next)

    def _load_elements(self, images, step=5):
      '''Generator to fill the listmodel of a treeview progressively.'''
      n = 0
      self.freeze_child_notify()
      for img_path in images:
          self.elements.append(Img_List.UI_Image(img_path).get_as_treeview_element())

	  # yield to gtk main loop once awhile
          n += 1
          if (n % step) == 0:
              self.thaw_child_notify()
              yield True
              #update the marker layers
              self.freeze_child_notify()

      self.thaw_child_notify()
      # stop idle_add()
      yield False

    class UI_Image(gobject.GObject):
        def __init__(self, path):
            gobject.GObject.__init__(self)
            self.path = path
            self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.path, 64, 64)

        def get_as_treeview_element(self):
            return [self, self._get_thumb(), self._get_name()]

        def as_image(self):
            return Image(self.path, self._get_name())

        def _get_thumb(self):
            return self.pixbuf

        def _get_name(self):
            return os.path.splitext(os.path.basename(self.path))[0]

