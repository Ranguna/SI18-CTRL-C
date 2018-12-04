import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class TreeView(Gtk.TreeView):
	def __init__(self):
		# model
		self.model = Gtk.ListStore.new([str])

		# view
		Gtk.TreeView.__init__(self, self.model)

		col_a = Gtk.TreeViewColumn('Clip History',
									Gtk.CellRendererText(),
									text=0)
		self.append_column(col_a)
	
	def appendData(self, data):
		self.model.append([data])

class Window(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title='Mein Gtk-Fenster')
		self.set_default_size(800, 600)

		self.view = TreeView()
		scroll = Gtk.ScrolledWindow()
		scroll.add (self.view)
		scroll.set_policy (Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		self.add (scroll)

		self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		self.clipboard.connect('owner-change',self.onClipChange)
		self.ignore_clip = False

		self.connect('destroy', Gtk.main_quit)
		self.show_all()

	def onClipChange(self, *args):
		if not self.ignore_clip:
			clip_data = self.clipboard.wait_for_text()
			# send clip data to list view
			self.view.appendData(clip_data)

			# replace clipboard with encrypted text
			self.clipboard.set_text(clip_data, -1)
			self.ignore_clip = True
		else:
			self.ignore_clip = False


if __name__ == '__main__':
	win = Window()
	Gtk.main()