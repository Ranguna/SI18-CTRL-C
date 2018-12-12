# encoding: utf-8
from pprint import pprint
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from os import path, urandom, listdir
import times
import re
import aes
import rsa
import hashez

files_location = "./"
file_prefix = "."
clip_sufix = "_clip"
hash_sufix = "_hash"
keypair_sufix = ".pem"
# if n files is changed, check load_users' for loop

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
		self.load_users()
		self.userCombo.connect('changed', self.onUserChange)
		userRowHbox.pack_start(self.userCombo, True, True, 0)
		self.newUserButton = Gtk.Button.new_with_label("New User")
		self.newUserButton.connect("clicked", self.newUser)
		userRowHbox.pack_start(self.newUserButton, True, True, 0)

		listbox.add(userRow)


		# button row selection
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

		self.selectionButtons["verificar"].connect("clicked",self.verifyEntry)


		# file button row
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		box_outer.pack_start(listbox, True, True, 0)

		self.fileButtons = {
			"verAssi": Gtk.Button.new_with_label("Verificar Ficheiro") # Verificar ficheiro
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

		self.ignoreUserChange = False

		self.loggedInUser = None
		self.keyPair = None
		# listbox_2.show_all()
	
	def verifyEntry(self,widget):
		if self.userCombo.get_active() == -1: # provavelmente nunca vai acontecer
			return 	

		dialog = SearchWindow(self)
		response = dialog.run()
		
		if(response == Gtk.ResponseType.OK):
			if not self.checkUserIntegrity(self.userCombo.get_active_text()):
				self.ignoreUserChange = True
				self.promptError("User inválido.", "Os ficheiros do utilizador foram corrompidos.")
				self.userCombo.remove(self.userCombo.get_active())
				self.loggedInUser = None
				self.keyPair = None
				return
		
			procurar = dialog.stringEntry.get_text()
			hash_file = files_location + file_prefix + self.userCombo.get_active_text() + hash_sufix
			info = "Entrada Não Existe"
			with open(hash_file,"r") as file:
				for line in file.readlines():
					line = line.strip()
					if hashez.verify(procurar, line):
		
						info = "Entrada Existente"							
			self.promptInfo("Verificação", info)			
		
		dialog.destroy()
	
	def checkUserIntegrity(self,user):
		# self.userCombo.remove(self.userCombo.get_active())
		if (not (
				path.isfile(files_location + file_prefix + user + clip_sufix) and
				path.isfile(files_location + file_prefix + user + hash_sufix) and
				path.isfile(files_location + file_prefix + user + keypair_sufix)
			)):
				# remover user do combo
				# try:
				# 	os.remove(files_location + file_prefix + user + clip_sufix)
				# except Exception:
				# 	pass
				# try:
				# 	os.remove(files_location + file_prefix + user + keypair_sufix)
				# except Exception:
				# 	pass
				# try:
				# 	os.remove(files_location + file_prefix + user + hash_sufix)
				# except Exception:
				# 	pass
				return False

		return True

	def load_users(self):
		self.clearCombo()
		users = {}
		for file in listdir(files_location):
			match = re.match(r"\.(.+)(%s|%s|%s)"%(clip_sufix,hash_sufix, keypair_sufix), file)
			if match != None:
				try:
					users[match.group(1)].update([match.group(2)])
				except Exception:
					users[match.group(1)] = set([match.group(2)])

		for user in users:
			if len(users[user]) == 3:
				self.userCombo.append(user, user)

	def promptError(self, Title, Desc):
		dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
			Gtk.ButtonsType.OK, Title)
		dialog.format_secondary_text(
			Desc)
		dialog.run()
		dialog.destroy()

	def promptInfo(self, Title, Desc):
		dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
			Gtk.ButtonsType.OK, Title)
		dialog.format_secondary_text(
			Desc)
		dialog.run()
		dialog.destroy()

	def onUserChange(self, widget):
		if self.ignoreUserChange:
			self.ignoreUserChange = False
			return

		loginOk = False
		response = Gtk.ResponseType.OK
		dialog  = None
		passwd = None
		print(widget.get_active_text())
		while not loginOk and response == Gtk.ResponseType.OK:
			if not self.checkUserIntegrity(widget.get_active_text()):
				self.ignoreUserChange = True
				self.promptError("User inválido.", "Os ficheiros do utilizador foram corrompidos.")
				self.loggedInUser = None
				self.keyPair = None
				self.userCombo.remove(self.userCombo.get_active())
				break
			
			dialog = LoginDialog(self, widget.get_active_text())
			response = dialog.run()

			loginOk = False
			if(response == Gtk.ResponseType.OK): # fez login
				print(dialog.passEntry.get_text()) # pass
				passwd = dialog.passEntry.get_text()
				# ver se tem todos os ficheiros
				if(not self.checkUserIntegrity(widget.get_active_text())):
					self.ignoreUserChange = True
					response == Gtk.ResponseType.OK
					self.promptError("User inválido.", "Os ficheiros do utilizador foram corrompidos.")
					self.userCombo.remove(self.userCombo.get_active())
					self.loggedInUser = None
					self.keyPair = None
					dialog.destroy()
					break
				
				clip_file = files_location + file_prefix + widget.get_active_text() + clip_sufix
		
				# ver se a pass corresponde ao ficheiro
				with open(clip_file, "r") as f:
					if not hashez.verify(passwd, f.readline().replace("\n","")):
						self.promptError("Password incorreta.", "A password introduzida está incorreta.")
					else:
						loginOk = True

			dialog.destroy()

		if loginOk:
			self.loggedInUser = widget.get_active_text()

			keypair_file = files_location + file_prefix + widget.get_active_text() + keypair_sufix
			clip_file = files_location + file_prefix + widget.get_active_text() + clip_sufix
			
			## carregar par de chaves
			try:
				self.keyPair = rsa.KeyPair(keypair_file, passwd)
			except Exception as err:
				print("Error while loading keys: " +err.message)
				# clear all user vars
				self.keyPair = None
				self.loggedInUser = None
				self.ignoreUserChange = True
				self.userCombo.set_active(-1)

			## carregar as entradas
			# apagar entradas antigas
			self.view.clearData()
			# carregar novas
			with open(clip_file, "r") as f:
				f.readline() #password line
				line = f.readline() # first history line
				while line != '':
					try:
						# time(epoch):criptogram:encRandomBytes
						self.view.appendData(times.strftime(float(line.split(":")[0])))
					except Exception as err:
						self.view.appendData("-- corrupted --")
					line = f.readline()

			print("OK")
		else:
			print("not logged")
			self.ignoreUserChange = True
			self.userCombo.set_active(-1)

	def newUser(self, widget):
		newUserOk = False
		response = Gtk.ResponseType.OK
		name = None
		passwd = None
		while not newUserOk and response == Gtk.ResponseType.OK:
			dialog = CreateAccountDialog(self)
			response = dialog.run()

			newUserOk = False
			if(response == Gtk.ResponseType.OK):
				name = dialog.nameEntry.get_text()
				passwd = dialog.passEntry.get_text()

				clip_file = files_location + file_prefix + dialog.nameEntry.get_text() + clip_sufix
				
				# ver se o ficheiro existe
				if not path.isfile(clip_file):
					if len(passwd) < 12: # pass pequena
						self.promptError("Password pequena.", "A password é demasiado pequena, >11.")
					elif len(name) == 0: # user em branco
						self.promptError("User vazio.", "O nome de utilizadore está em branco.")
					else: # ok (y)
						newUserOk = True
				else: # se o ficheiro existe com o nome do user, user ja existe
					self.promptError("Utilizador já existente.", "O utilizador inserido já se econtra registado.")

			dialog.destroy()

		if newUserOk:
			self.loggedInUser = name
			clip_file = files_location + file_prefix + name + clip_sufix
			hash_file = files_location + file_prefix + name + hash_sufix
			keypair_file = files_location + file_prefix + name + keypair_sufix
			
			# gerar a guardar par de chaves rsa
			self.keyPair = rsa.KeyPair(keypair_file, passwd, True)
			with open(clip_file, "w") as f:
				# cria ficheiro do clip e mete lá a pass com uma pitadinha de sal
				f.write(hashez.salted(passwd)+"\n")
			open(hash_file,"w").close() # cria um ficheiro vazio de hashes
			

			# add user to box
			# a funcao de mudar o utilizador no combobox vai ser executada
			# dizer para nao pedir a pass porque o utilizador acabou de a meter
			self.ignoreUserChange = True
			# adicionar user
			self.userCombo.append(name,name)
			# meter como selecionado
			self.userCombo.set_active_id(name)

	def onSelection(self, treeview):
		# não fazer nada se nenhum utilizador estiver ligado
		if self.userCombo.get_active() == -1:
			for _, button in self.selectionButtons.items():
				button.set_sensitive(True)
			return

		a,b =treeview.get_selection().get_selected_rows()
		for _, button in self.selectionButtons.items():
			button.set_sensitive(True)
		# print("a ", a[b[0]][0])

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
			# send clip data to list view
			# self.view.appendData(clip_data)

			# do msg encryption scheme
			msg = self.clipboard.wait_for_text()
			randomBytes = urandom(min(self.keyPair.publicKey.size()/8, len(msg))).encode("hex")
			
			criptogram = aes.AESCipher(randomBytes).encrypt(msg)
			encRandomBytes = self.keyPair.encrypt(randomBytes)

			encMsg = criptogram + ":"+ encRandomBytes

			entryTime = times.epochtime()
			msgEntry = str(entryTime) + ":"+ encMsg

			# save to end of file
			if not self.checkUserIntegrity(self.userCombo.get_active_text()):
				self.ignoreUserChange = True
				self.promptError("User inválido.", "Os ficheiros do utilizador foram corrompidos.")
				self.userCombo.remove(self.userCombo.get_active())
				self.loggedInUser = None
				self.keyPair = None
				return
			
			# clip history
			with open(files_location + file_prefix + self.userCombo.get_active_text() + clip_sufix, "a") as f:
				f.write(msgEntry+"\n")

			# hash log
			with open(files_location + file_prefix + self.userCombo.get_active_text() + hash_sufix, "a") as f:
				f.write(hashez.salted(msg)+"\n")

			# add entry to view
			self.view.appendData(times.strftime(entryTime))
		else:
			self.ignore_clip = False

	def clearCombo(self):
		self.userCombo.get_model().clear()
	 

win = ListBoxWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
