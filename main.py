# encoding: utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import aes

files_location = "./"
file_prefix = "."
clip_sufix = "_clip"
hash_sufix = "_hash"

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
	
	def appendData(self, info):
		self.model.append([info])


class ListBoxWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="CTRL+C: Um Gestor de Clipboard Porreirinho")
		self.set_default_size(400, 200)
		self.set_border_width(10)

		box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(box_outer)

		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		box_outer.pack_start(listbox, True, True, 0)

		userRow = Gtk.ListBoxRow()
		userRowHbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
		userRow.add(userRowHbox)
		userRowHbox.pack_start(Gtk.Label(""), True, True, 0)
		self.userCombo = Gtk.ComboBoxText()
		self.userCombo.connect('changed', self.onUserChange)
		self.userCombo.append("1","asd")
		userRowHbox.pack_start(self.userCombo, True, True, 0)
		self.newUserButton = Gtk.Button.new_with_label("New User")
		self.newUserButton.connect("clicked", self.newUser)
		userRowHbox.pack_start(self.newUserButton, True, True, 0)

		listbox.add(userRow)


		# selection button row
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		box_outer.pack_start(listbox, True, True, 0)

		self.selectionButtons = {
			"copiar": Gtk.Button.new_with_label("Copiar"), #!!! FAZER - a copia
			"verificar": Gtk.Button.new_with_label("Verificar"), #!!! FAZER - Verifcar o hash
			"apagar": Gtk.Button.new_with_label("Apagar") #!!! FAZER - apagar entrada  do coiso
		}
		selectionButton = Gtk.ListBoxRow()
		selectionButtonHbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
		selectionButton.add(selectionButtonHbox)
		for _, button in self.selectionButtons.items():
			selectionButtonHbox.pack_start(button, True, True, 0)
			button.set_sensitive(False)
		listbox.add(selectionButton)



		# file button row
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		box_outer.pack_start(listbox, True, True, 0)

		self.fileButtons = {
			"verAssi": Gtk.Button.new_with_label("Verificar Ficheiro")
		}
		fileButton = Gtk.ListBoxRow()
		fileButtonHbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
		fileButton.add(fileButtonHbox)
		for _, button in self.fileButtons.items():
			fileButtonHbox.pack_start(button, True, True, 0)
		listbox.add(fileButton)


		# clipboard history
		self.view = TreeView()
		scroll = Gtk.ScrolledWindow()
		scroll.set_min_content_height(500)
		scroll.add (self.view)
		scroll.set_policy (Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		# self.add(scroll)
		
		self.view.connect("row-activated", self.onClickClipSelection)
		self.view.connect('cursor-changed', self.onSelection)

		box_outer.pack_start(scroll, True, True, 0)

		self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		self.clipboard.connect('owner-change',self.onClipChange)
		self.ignore_clip = False


		self.loggedInUser = None
		self.currentHashedPass = None
		# listbox_2.show_all()
	

	def promptError(self, Title, Desc):
		dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
			Gtk.ButtonsType.CANCEL, Title)
		dialog.format_secondary_text(
			Desc)
		dialog.run()
		dialog.destroy()

	def onUserChange(self, widget):
		dialog = LoginDialog(self, widget.get_active_text())
		response = dialog.run()

		loginOk = False
		if(response == Gtk.ResponseType.OK): # fez login
			print(dialog.passEntry.get_text()) # pass
			#!!! FAZER - Login aqui
			# ver se a pass corresponde ao ficheiro
			# carregar as entradas
			# se a pass nao corresponder, mostrar isto:
			# self.promptError("Password errada", "A password introduzida está errada.")

		if(loginOk or response == Gtk.ResponseType.CANCEL):
			self.loggedInUser = widget.get_active_text()
			#!!! FAZER - fazer hash da pass e guardar em:
			# self.currentHashedPass = HASH DE PASS AQUI
			dialog.destroy()

	def newUser(self, widget):
		dialog = CreateAccountDialog(self)
		response = dialog.run()

		newUserOk = False
		if(response == Gtk.ResponseType.OK):
			print(dialog.nameEntry.get_text()) # nome
			print(dialog.passEntry.get_text()) # pass
			#!!! FAZER - Criar conta aqui
			# procurar se j]a existe um ficheiro com aquele nome
			# fazer o hash da pass com sal, meter na primeira linha do ficheiro
			# se o user já existir então fazer:
			# self.promptError("Utilizador já existente.", "O utilizador inserido já se econtra registado.")

		if(newUserOk or response == Gtk.ResponseType.CANCEL):
			self.loggedInUser = dialog.nameEntry.get_text()
			#!!! FAZER - fazer hash da pass e guardar em:
			# self.currentHashedPass = HASH DE PASS AQUI
			dialog.destroy()

	def onSelection(self, treeview):
		# não fazer nada se nenhum utilizador estiver ligado
		if self.userCombo.get_active() == -1:
			for _, button in self.selectionButtons.items():
				button.set_sensitive(True)
			return

		a,b =treeview.get_selection().get_selected_rows()
		for _, button in self.selectionButtons.items():
			button.set_sensitive(True)
		print("a ", a[b[0]][0])

	def onClickClipSelection(self, widget, row, col):
		# não fazer nada se nenhum utilizador estiver ligado
		if self.userCombo.get_active() == -1:
			return False

		print(self.view.model[row][:][0])
		return True

	def onClipChange(self, *args):
		# não fazer nada se nenhum utilizador estiver ligado
		if self.userCombo.get_active() == -1:
			return 

		if not self.ignore_clip:
			clip_data = self.clipboard.wait_for_text()
			# send clip data to list view
			self.view.appendData(clip_data)

			#!!! FAZER - Meter entradas no ficheiro aqui
			#  A nova entrada fica no fim do ficheiro com o nome self.userCombo.get_active_text(), ou algo do genero
			# mete o hash no ficheiro dos hashes tambem
			# a nove entrada do clipboard está na variavel clip_data

			# replace clipboard with encrypted text
			self.clipboard.set_text(clip_data, -1)
			self.ignore_clip = True
		else:
			self.ignore_clip = False

	def clearCombo(self):
		self.userCombo.get_model().clear()
	

class EntriesFileHandler():
	def __init__(self, filename):
		self.inited = False
		try:
			self.clipEntries = open("."+filename+"_clip", "a")
			self.hashEntries = open("."+filename+"_hash", "a")
			self.inited = True
		except IOError:
			print("File not found")

	def newEntry(self, time, data):
		if(not self.inited):
			return

		self.clipEntries.write()

	
	def closeFiles(self):
		if(not self.inited):
			return

		self.clipEntries.close()
		self.hashEntries.close()
	 

win = ListBoxWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()