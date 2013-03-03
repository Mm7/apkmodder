#  
#  Welcome to MM7 Android Application Modder
#

print('--------------------------------------------------------------')
print('')
print('APK MODDER BY')
print('_   _  _    _ __')
print('|\  /| |\  /|  /')
print('| \/ | | \/ | / ')
print('')
print('--------------------------------------------------------------')

print('WARNING: ALPHA STAGE. MANY BUGS')

try:
	import sys
except:
	print("FATAL : Can't import sys O.o Impossible XD")
try:
	import gtk
	import pygtk
except:
	print("FATAL : Can't import gtk")
	sys.exit(0)
try:
	import zipfile
except:
	print("FATAL : Can't import zipfile")
	sys.exit(0)
try:
	import tempfile
except:
	print("FATAL : Can't import tempfile")
	sys.exit(0)
try:
	import os
except:
	print("FATAL : Can't import os O.o Impossible XD")
	sys.exit(0)
try:
	import Image
except:
	print("FATAL : Can't import Image")
	sys.exit(0)
try:
	import shutil
except:
	print("FATAL : Can't import shutil")
	sys.exit(0)


tempdir = tempfile.gettempdir()

def GetImageSize(image):
	size = image.size()
	return(size[0], size[1])

def Resize(limage, dim=None):
	for image in limage:	
		im1 = Image.open(tempdir+'/apkmoddertmp/'+image)
		im2 = im1.resize((50, 50), Image.ANTIALIAS)	
		im2.save(tempdir+'/apkmoddertmp/'+image+'resized.png')

def GetZipDrawableFileName(limage, drawable):
	limageindir	= []
	for image in limage:
		if drawable in image:
			limageindir.append(image)
	return(limageindir)

def GetZipFileName(zz):
	lfile = []
	for zfile in zz.namelist():
		if zfile.endswith('/'):
			continue
		else:
			lfile.append(zfile)
	return(lfile)

def GetZipDrawableName(lfile):
	ldrawable = []	
	for directory in lfile:
		if 'drawable' in directory:
			ldsplit = directory.split('/')
			for ldsplit in ldsplit:
				if 'drawable' in ldsplit:
					if (ldrawable.__contains__(ldsplit)) is False:							
						ldrawable.append(ldsplit)
	return(ldrawable)

def GetZipImageName(lfile):
	limage = []
	for image in lfile:
		if image.endswith('.png') or image.endswith('.jpg'):
			limage.append(image)
	return(limage)

def ZipWrite(zz, filepath, directory=None):
	if directory:
		zz.write(filepath, directory+'/'+(os.path.basename(filepath)))		
	else:	
		zz.write(os.path.basename(filepath))

def Extract(zz):
	zz.extractall(tempdir+'/apkmoddertmp')

class MyWindow(gtk.Window):

	apki = False
	apko = False

	def __init__(self):
		gtk.Window.__init__(self)

		self.set_default_size(1200, 800)		
		self.set_position(gtk.WIN_POS_CENTER)		

		vbox = gtk.VBox(False, 10)	

		mb = gtk.MenuBar()

		filemenu = gtk.Menu()
		filem = gtk.MenuItem("_File")
		filem.set_submenu(filemenu)

		agr = gtk.AccelGroup()
		self.add_accel_group(agr)

		newi = gtk.ImageMenuItem(gtk.STOCK_NEW, agr)
		key, mod = gtk.accelerator_parse("<Control>N")
		newi.add_accelerator("activate", agr, key, 
    	mod, gtk.ACCEL_VISIBLE)
		filemenu.append(newi)

		openi = gtk.MenuItem(label = 'Open input apk')
		key, mod = gtk.accelerator_parse("<Control>I")
		openi.add_accelerator("activate", agr, key, 
    	mod, gtk.ACCEL_VISIBLE)
		openi.connect('activate', self.OnOpen, 0)

		filemenu.append(openi)

		openm = gtk.MenuItem(label = 'Open output apk')
		key, mod = gtk.accelerator_parse("<Control>O")
		openm.add_accelerator("activate", agr, key, 
    	mod, gtk.ACCEL_VISIBLE)
		openm.connect('activate', self.OnOpen, 1)

		filemenu.append(openm)

		sep = gtk.SeparatorMenuItem()
		filemenu.append(sep)

		exit = gtk.ImageMenuItem(gtk.STOCK_QUIT, agr)
		key, mod = gtk.accelerator_parse("<Control>Q")
		exit.add_accelerator("activate", agr, key, 
    	mod, gtk.ACCEL_VISIBLE)

		exit.connect("activate", self.Close)

		filemenu.append(exit)

		mb.append(filem)
		vbox.pack_start(mb, False, False, 5)	
	
		hseparator1 = gtk.HSeparator()

		vbox.pack_start(hseparator1, False, False, 0)

		hbox1 = gtk.HBox(True, 10)		

		self.combobox1 = gtk.combo_box_new_text()	
		self.combobox1.connect('changed', self.changed_cbI)	

		hbox1.pack_start(self.combobox1, False, False, 0)

		self.combobox2 = gtk.combo_box_new_text()	
		self.combobox2.connect('changed', self.changed_cbO)	

		hbox1.pack_start(self.combobox2, False, False, 0)
		vbox.pack_start(hbox1, False, False, 0)

		hseparator2 = gtk.HSeparator()
		vbox.pack_start(hseparator2, False, False, 0)

		hbox2 = gtk.HBox(True, 10)		

		scrolled_window1 = gtk.ScrolledWindow()
		hbox2.pack_start(scrolled_window1, True, True, 0)		
		scrolled_window1.show()
		
		self.table1 = gtk.Table(2, 2, True)

		self.image1 = gtk.Image()
		self.image1.set_from_file("/home/marco/workspace/img.png")	
		self.image1.show()

		self.table1.attach(self.image1, 0, 2, 0, 2)

		scrolled_window1.add_with_viewport(self.table1)
		self.table1.show()

		scrolled_window2 = gtk.ScrolledWindow()
		hbox2.pack_start(scrolled_window2, True, True, 0)		
		scrolled_window2.show()
		
		self.table2 = gtk.Table(2, 2, False)

		self.image2 = gtk.Image()
		self.image2.set_from_file("/home/marco/workspace/img.png")	
		self.image2.show()
		
		self.table2.attach(self.image2, 0, 2, 0, 2)

		scrolled_window2.add_with_viewport(self.table2)
		self.table2.show()

		vbox.pack_start(hbox2, True, True, 0)

		hseparator3 = gtk.HSeparator()		
		vbox.pack_start(hseparator3, False, False, 0)

		hbox3 = gtk.HBox(False, 10)

		button1 = gtk.Button(label="Button 1")
		button2 = gtk.Button(label="Button 2")

		hbox3.pack_end(button1, False, False, 0)		
		hbox3.pack_end(button2, False, False, 0)

		vbox.pack_start(hbox3, False, False, 0)

		self.add(vbox)

		self.connect("delete-event", self.Close)

	def Close(self, b, c):
		if os.path.exists(tempdir+'/apkmoddertmp'):
			shutil.rmtree(tempdir+'/apkmoddertmp')
		gtk.main_quit()

	def changed_cbI(self, combobox):
		model = combobox.get_model()	
		index = combobox.get_active()
		for imageob in self.liimageob:
			self.table1.remove(imageob)
		for checkbutton in self.lcheckbuttonob:
			self.table1.remove(checkbutton)
		if index:
			ldirfname = GetZipDrawableFileName(self.liimage, model[index][0])
			self.DrawI(ldirfname)	

	def changed_cbO(self, combobox):
		model = combobox.get_model()	
		index = combobox.get_active()
		for imageob in self.loimageob:
			self.table2.remove(imageob)
		for label in self.llabelob:
			self.table2.remove(label)
		if index:
			ldirfname = GetZipDrawableFileName(self.loimage, model[index][0])
			self.DrawO(ldirfname)				


	def OnOpen(self, a, b):
		if (b == 0) and (self.apki == False):
					
			dialog = gtk.FileChooserDialog("Open..",
            	                   None,
            	                   gtk.FILE_CHOOSER_ACTION_OPEN,
            	                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            	                    gtk.STOCK_OPEN, gtk.RESPONSE_OK))
			dialog.set_default_response(gtk.RESPONSE_OK)
			response = dialog.run()
			self.pathi = dialog.get_filename()
			dialog.destroy()
			self.apki = True
			self.zinput = zipfile.ZipFile(self.pathi)
			self.lifile = GetZipFileName(self.zinput)
			self.lidrawable = GetZipDrawableName(self.lifile)			
			for dirdrawable in self.lidrawable:
				self.combobox1.append_text(dirdrawable)
			self.table1.remove(self.image1)
			self.liimage = GetZipImageName(self.lifile)
			Extract(self.zinput)
			Resize(self.liimage)
			lidirfname = GetZipDrawableFileName(self.liimage, self.lidrawable[0])
			self.DrawI(lidirfname)

		elif (b == 0) and (self.apki == True):		
			md = gtk.MessageDialog(self, 
				gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
				gtk.BUTTONS_CLOSE, "File already selected")
			md.run()
			md.destroy()

		elif (b == 1) and (self.apko == False):
			dialog = gtk.FileChooserDialog("Open..",
            	                   None,
            	                   gtk.FILE_CHOOSER_ACTION_OPEN,
            	                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            	                    gtk.STOCK_OPEN, gtk.RESPONSE_OK))
			dialog.set_default_response(gtk.RESPONSE_OK)
			response = dialog.run()
			self.patho = dialog.get_filename()
			dialog.destroy()
			self.apko = True
			self.zoutput = zipfile.ZipFile(self.patho)
			self.lofile = GetZipFileName(self.zoutput)
			self.lodrawable = GetZipDrawableName(self.lofile)		
			for dirdrawable in self.lodrawable:
				self.combobox2.append_text(dirdrawable)
			self.table2.remove(self.image2)
			self.loimage = GetZipImageName(self.lofile)
			Extract(self.zoutput)
			Resize(self.loimage)
			lodirfname = GetZipDrawableFileName(self.loimage, self.lodrawable[0])
			self.DrawO(lodirfname)

		elif (b == 1) and (self.apko == True):
			md = gtk.MessageDialog(self, 
				gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
				gtk.BUTTONS_CLOSE, "File already selected")
			md.run()
			md.destroy()
		
		else:
			md = gtk.MessageDialog(self, 
				gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
				gtk.BUTTONS_CLOSE, "Bug here!! : OnOpen Else !!")
			md.run()
			md.destroy()
			sys.exit(0)		

	def DrawI(self, limage):		
		a=0
		b=1
		c=-1
		self.liimageob = []
		self.lcheckbuttonob = []
		self.diob = {}
		for image in limage:
			a=a+1
			c=c+1
			if a > 3:
				b=b+2
				a=1
			self.image1 = gtk.Image()		
			self.image1.set_from_file(tempdir+'/apkmoddertmp/'+image+'resized.png')
			self.image1.show()
			self.diob[image] = self.image1
			self.table1.attach(self.image1, a-1, a, b-1, b)
			self.liimageob.append(self.image1)
			self.checkbutton1 = gtk.CheckButton(image) 
			self.checkbutton1.show()
			self.checkbutton1.connect('clicked', self.Match, self.liimageob[c], image)
			self.table1.attach(self.checkbutton1, a-1, a, b, b+1)	
			self.lcheckbuttonob.append(self.checkbutton1)

	def DrawO(self, limage):		
		a=0
		b=1
		c=-1
		self.loimageob = []
		self.llabelob = []
		self.doob = {}
		for image in limage:
			a=a+1
			c=c+1
			if a > 3:
				b=b+2
				a=1
			self.image2 = gtk.Image()		
			self.image2.set_from_file(tempdir+'/apkmoddertmp/'+image+'resized.png')
			self.image2.show()
			self.doob[image] = self.image2
			self.table2.attach(self.image2, a-1, a, b-1, b)
			self.label = gtk.Label(image)
			self.label.show()
			self.table2.attach(self.label, a-1, a, b, b+1)
			self.llabelob.append(self.label)

	def Match(self, widget, image, imagename):
		if widget.get_active():
			if self.apko is True:
				imagebn = os.path.basename(imagename)
				mok = False
				for image2 in self.loimage:
					if imagebn in image2:
						mok = True
						ob = (self.diob[imagename])
						w, h = ob.size()
						print(w)
						print(h)
						#print(isize)
				if mok is False:
				  print('False')
				#if any(imagebn in s for s in self.loimage):		
					#print(GetImageSize(self.loimageob)[0])
			else:
				md = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "No apk theme selected")
				md.run()
				md.destroy()
				widget.set_active(False)
			


#zz = zipfile.ZipFile('/home/marco/workspace/Nfc.zip', 'a')
#lfile = GetZipFileName(zz)
#ldrawable = GetZipDrawableName(lfile)
#ZipWrite(zz, '/home/marco/workspace/img.png', 'xd')
#zz.close()

win = MyWindow()
win.show_all()
gtk.main()
