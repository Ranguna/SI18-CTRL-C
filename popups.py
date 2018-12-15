# encoding: utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class CreateAccountDialog(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "Nova Conta", parent, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 "Criar", Gtk.ResponseType.OK))

		self.set_default_size(150, 100)
		self.set_border_width(10)

		box = self.get_content_area()

		label = Gtk.Label("Nome: ")
		label.set_alignment(0, 0.5)
		box.add(label)
		
		self.nameEntry = Gtk.Entry()
		box.add(self.nameEntry)

		label = Gtk.Label("Password: ")
		label.set_alignment(0, 0.5)
		box.add(label)
		
		self.passEntry = Gtk.Entry()
		self.passEntry.set_visibility(False)
		box.add(self.passEntry)

		self.show_all()


class SearchWindow(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "Verificar", parent, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 "Procurar", Gtk.ResponseType.OK))

		self.set_default_size(150, 100)
		self.set_border_width(10)

		box = self.get_content_area()
		
		label = Gtk.Label("Texto: ")
		label.set_alignment(0, 0.5)
		box.add(label)
		
		self.stringEntry = Gtk.Entry()
		self.stringEntry.set_visibility(True)
		box.add(self.stringEntry)

		self.show_all()

class LoginDialog(Gtk.Dialog):
	def __init__(self, parent, nome):
		Gtk.Dialog.__init__(self, "Entrar", parent, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 "Entrar", Gtk.ResponseType.OK))

		self.set_default_size(150, 100)
		self.set_border_width(10)

		box = self.get_content_area()

		label = Gtk.Label("Nome: ")
		label.set_alignment(0, 0.5)
		box.add(label)
		
		label = Gtk.Label(nome)
		label.set_alignment(0, 0.5)
		box.add(label)

		label = Gtk.Label("Password: ")
		label.set_alignment(0, 0.5)
		box.add(label)
		
		self.passEntry = Gtk.Entry()
		self.passEntry.set_visibility(False)
		box.add(self.passEntry)

		self.show_all()


class TreeView(Gtk.TreeView):
	def __init__(self):
		# model
		self.activate_on_single_click = True
		self.model = Gtk.ListStore.new([str])

		# view
		Gtk.TreeView.__init__(self, self.model)

		col_a = Gtk.TreeViewColumn('Histórico de Clipboard',
									Gtk.CellRendererText(),
									text=0)
		self.append_column(col_a)
	
	def appendData(self, data):
		self.model.append([data])
	
	def clearData(self):
		self.model.clear()

