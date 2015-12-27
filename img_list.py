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
        column_pixbuf = gtk.TreeViewColumn('Image', gtk.CellRendererPixbuf(), pixbuf=1)
        self.append_column(column_pixbuf)
        column_text = gtk.TreeViewColumn('Name', gtk.CellRendererText(), text=2)
        self.append_column(column_text)

        # Provide a nice scrollable window for the users convenience but still extend
        # a TreeView: most of the functionality a caller would need is in there, so
        # making this class extend a ScrolledWindow would require a lot of scaffolding
        self.vscroll = gtk.ScrolledWindow()
        self.vscroll.set_policy(hscrollbar_policy=gtk.POLICY_NEVER, vscrollbar_policy=gtk.POLICY_AUTOMATIC)
        self.vscroll.add_with_viewport(self)

        # Handle custom tooltips
        self._tooltips = Img_List.Tooltip_Handler(self, 
                                                  self._on_tooltip_triggered,
                                                  self._on_tooltip_gone)

        self.set_path(start_path)

    def _on_tooltip_triggered(self, tree_path):
        print self.elements.get_value(self.elements.get_iter(tree_path), 0)

    def _on_tooltip_gone(self):
        print "/tooltip"

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
            if filename.upper().endswith('JPG') or filename.upper().endswith('PNG'):
                images.append(os.path.join(path, filename))

        loader = self._load_elements(images)
        glib.idle_add(loader.next)

    def _load_elements(self, images, step=5):
      """Generator to fill the listmodel of a treeview progressively."""
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

    class Tooltip_Handler(object):
        def __init__(self, treeview_obj, on_tooltip_triggered, on_tooltip_gone):
            # Set listeners to detect tooltip event
            treeview_obj.connect('motion-notify-event', self._on_mouse_move)
            treeview_obj.connect('leave-notify-event', self._on_mouse_exit)

            self._on_tooltip_triggered = on_tooltip_triggered
            self._on_tooltip_gone = on_tooltip_gone
            self._treeview_obj = treeview_obj

            self._tooltip_delay = gtk.Tooltips().delay # Use default wait
            self._tooltip_position = None
            self._tooltip_countdown = None
            self._tooltip_active = False

        def _on_mouse_move(self, widget, data=None):
            self._stop_active_tooltips()
            if self._tooltip_countdown is not None:
                gobject.source_remove(self._tooltip_countdown)

            self._tooltip_countdown = gobject.timeout_add(self._tooltip_delay, self._trigger_tooltip)
            self._tooltip_position = (int(data.x), int(data.y))

        def _on_mouse_exit(self, widget, data=None):
            self._stop_active_tooltips()
            if self._tooltip_countdown is not None:
                gobject.source_remove(self._tooltip_countdown)
                self._tooltip_countdown = None

        def _stop_active_tooltips(self):
            if not self._tooltip_active:
                return

            self._on_tooltip_gone()
            self._tooltip_active = False

        def _trigger_tooltip(self):
            self._tooltip_countdown = None
            mouse_over_row = self._treeview_obj.get_path_at_pos(\
                                        self._tooltip_position[0], \
                                        self._tooltip_position[1])
            tree_path = mouse_over_row[0]
            self._tooltip_active = True
            self._on_tooltip_triggered(tree_path)

