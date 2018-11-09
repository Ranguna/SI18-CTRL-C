import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

ignore_clip = False
def callBack(*args):
  if clip.wait_for_text() == "quit":
    return Gtk.main_quit()
  global ignore_clip
  print("Clipboard changed. New value = " + clip.wait_for_text())
  if not ignore_clip:
    clip.set_text("hello",-1)
    ignore_clip = True
  else:
    ignore_clip = False

clip.connect('owner-change',callBack)
Gtk.main()
