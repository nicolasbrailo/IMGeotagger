import gtk
import glib
import os

class Img_List(gtk.TreeView):
    def __init__(self):
        self.liststore = gtk.ListStore(int, gtk.gdk.Pixbuf, str, str)
        gtk.TreeView.__init__(self, self.liststore)

        self.set_model(self.liststore)
        self.set_tooltip_column(3)
        #self.get_selection().set_mode(gtk.SelectionMode.MULTIPLE)

        #cell renderers for image and image name
        column_pixbuf = gtk.TreeViewColumn("Image", gtk.CellRendererPixbuf(), pixbuf=1)
        self.append_column(column_pixbuf)
        column_text = gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=2)
        self.append_column(column_text)

    def set_path(self, path):
        self.liststore.clear()

        images = list()
        if os.path.isdir(path):
            lst = os.listdir(path)
            lst.sort()
            for filename in lst:
                if filename.upper().endswith("JPG") or filename.upper().endswith("PNG"):
                    images.append(os.path.join(path, filename))

        loader = self.liststore_fill(images)
        glib.idle_add(loader.next)

    def liststore_fill(self, images, step=5):
      '''Generator to fill the listmodel of a treeview progressively.'''
      n = 0
      self.freeze_child_notify()
      for img in images:
          #fill the liststore model
          pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(img, 64, 64)
          self.liststore.append([42, pixbuf, os.path.splitext(os.path.basename(img))[0], "2/2/12"])

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

