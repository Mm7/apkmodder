#!/usr/bin/python2.7

#  Welcome to MM7 Android Application Modder

#Print lots information
print('+--------------------+')
print('|    APK MODDER      |')
print('+--------------------+')
print('')
print(' Alpha 2')
print(' Unstable version')
print('')
print('## All credits to mm7 (creator) and libs developer ##')
print('Source: https://github.com/Mm7/apkmodder')

#Import libraries

try:
	import sys
except:
	print("FATAL : Can't import sys O.o Impossible XD")
try:
	import os
except:
	print("FATAL : Can't import os O.o Impossible XD")
	sys.exit(0)
try:
	import logging
except:
	print("FATAL : Can't import logging")
	sys.exit(0)
	
# Inizialize log

if os.path.exists('log'):
	os.remove('log')

logger = logging.getLogger('myprogram')
hdlr = logging.FileHandler('log')
formatter = logging.Formatter('[%(levelname)s] %(message)s')
 
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
 
logger.info('Log system start')

# Import libraries

try:
	import gtk
	import pygtk
	logger.info('Gtk imported')
except:
	logger.error("Can't import gtk")
	print("FATAL : Can't import gtk")
	sys.exit(0)
try:
	import zipfile
	logger.info('ZipFile imported')
except:
	logger.error("Can't import zipfile")
	print("FATAL : Can't import zipfile")
	sys.exit(0)
try:
	import tempfile
	logger.info('Tempfile imported')
except:
	logger.error("Can't import tempfile")
	print("FATAL : Can't import tempfile")
	sys.exit(0)
try:
	import Image
	logger.info('Image imported')
except:
	logger.error("Can't import image")
	print("FATAL : Can't import Image")
	sys.exit(0)
try:
	import shutil
	logger.info('Shutil imported')
except:
	logger.error("Can't import shutil")
	print("FATAL : Can't import shutil")
	sys.exit(0)
try:
	import re
	logger.info('Re imported')
except:
	logger.error("Can't import re")
	print("FATAL : Can't import re")
	sys.exit(0)
try:
	import subprocess
	logger.info('Subprocess imported')
except:
	logger.error("Can't import subprocess")
	print("FATAL : Can't import subprocess")
	sys.exit(0)

# Get the tempdir of the host system
tempdir = tempfile.gettempdir()

#Declare some function

def GetImageSize(path):
	""" Get the image size (in pixels)
	
	Arg:
	    path of image
	    
	Return:
	    tuple of dimensions of image
	"""
	
	image = Image.open(path)
	x, y = image.size
	return(x, y)

def GetPath():
	""" Create a dialog which ask a path
	  
	Arg:
	    None
	    
	Return:
	    Path
	"""
	dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
	dialog.set_default_response(gtk.RESPONSE_OK)
	response = dialog.run()
	path = dialog.get_filename()

	dialog.destroy()
	return(path)
	
def GetDrawable(number):
	""" Get name of drawable folders in apk mod
	
	Arg:
	    number: mod or theme
	    
	Return:
	    List of drawable folders
	"""
	drawable=[]
	
	if number == 1:
		for root, dirs, files in os.walk(tempdir+'/apkmodder-mod/res'):
			if root == tempdir+'/apkmodder-mod/res':
				drawable = [ rdir for rdir in dirs if re.search(r'drawable-\w+', rdir, re.M|re.I) ]
	elif number == 2:
		for root, dirs, files in os.walk(tempdir+'/apkmodder-theme/res'):
			if root == tempdir+'/apkmodder-theme/res':
				drawable = [ rdir for rdir in dirs if re.search(r'drawable-\w+', rdir, re.M|re.I) ]
					
	return(drawable)
	
def GetDrawableFiles(drawable, number):
	""" Get the corrispondence between drawable directory and the files that contain
	
	Arg:
	    drawables list and number of mod or theme
	    
	Return:
	    dictionary with corrispondence
	"""

	d = {}
	
	if number == 1:
		for a in drawable:
			files = [ f for f in os.listdir(tempdir+'/apkmodder-mod/res/'+a) if (os.path.isfile(os.path.join(tempdir+'/apkmodder-mod/res/'+a,f))) and (os.path.splitext(os.path.join(tempdir+'/apkmodder-mod/res/'+a,f))[1] == '.png') ]
			d[tempdir+'/apkmodder-mod/res/'+a]=files
	elif number == 2:
		for a in drawable:
			files = [ f for f in os.listdir(tempdir+'/apkmodder-theme/res/'+a) if (os.path.isfile(os.path.join(tempdir+'/apkmodder-theme/res/'+a,f))) and (os.path.splitext(os.path.join(tempdir+'/apkmodder-theme/res/'+a,f))[1] == '.png') ]
			d[tempdir+'/apkmodder-theme/res/'+a]=files  
			
	return(d)

def SetCombobox(self, number, text, first):
	""" Set the combo box
	
	Args:
	    self, number of combobox, text to set, and first (used for active the combobox at open of apk)
	 
	Return:
	    anything
	"""
	if (number == 1) and first:
		self.combobox1.append_text(text)
		self.combobox1.set_active(0)
	elif (number == 1) and (not first):
		self.combobox1.append_text(text)
	elif (number == 2) and first:
		self.combobox2.append_text(text)
		self.combobox2.set_active(0)
	elif (number == 2) and (not first):
		self.combobox2.append_text(text)
		
def ResizeToDraw(diz):
	""" Resize image for prepering the draw
	
	Arg:
	    dictionary with corrispondence between image and dirs
	    
	Return:
	    anything
	"""
	for key in diz:
		for value in diz[key]:
			subprocess.call(['convert',key+'/'+value, '-resize', '50x50', key+'/'+value+'resized.png'])	
			
def GetImageToDraw(diz, dirs, number):
	""" Get a list of image in a particular drawable
	
	Args:
	    dictionary with corrispondence between image and dirs, drawable (string like drawable-mdpi), number 1 or 2 for mod or theme.
	    
	Return:
	    list of image
	"""
	limage = []
	if number == 1:
		for value in diz[tempdir+'/apkmodder-mod/res/'+dirs]:
			limage.append(tempdir+'/apkmodder-mod/res/'+dirs+'/'+value)
			limage.sort()
	if number == 2:
		for value in diz[tempdir+'/apkmodder-theme/res/'+dirs]:
			limage.append(tempdir+'/apkmodder-theme/res/'+dirs+'/'+value)
			limage.sort()
	return(limage)	

# Create main class
	
class MyWindow(gtk.Window):

	# Creato two booleans, when False apk not opened yet, when True apk opened
	apki = False
	apko = False

	# Define constructor
	def __init__(self):
		""" Create window layout
		
		Arg:
		    self
		
		Return:
		    anything
		"""
		
		# Create a window
		gtk.Window.__init__(self)

		# Set window size and position
		self.set_default_size(1200, 800)		
		self.set_position(gtk.WIN_POS_CENTER)		

		# Create main box container (vertical)
		vbox = gtk.VBox(False, 10)	

		# Create the menu bar
		mb = gtk.MenuBar()

		# Create menu
		filemenu = gtk.Menu()
		filem = gtk.MenuItem("_File")
		filem.set_submenu(filemenu)

		# Create accelerator group
		agr = gtk.AccelGroup()
		self.add_accel_group(agr)

		# Create a item and accelerator
		openi = gtk.MenuItem(label = 'Open mod apk')
		key, mod = gtk.accelerator_parse("<Control>I")
		openi.add_accelerator("activate", agr, key, 
    	mod, gtk.ACCEL_VISIBLE)
		openi.connect('activate', self.OnOpenI)

		# Append to menu
		filemenu.append(openi)

		# Create a item and accelerator
		openm = gtk.MenuItem(label = 'Open theme apk')
		key, mod = gtk.accelerator_parse("<Control>O")
		openm.add_accelerator("activate", agr, key, 
    	mod, gtk.ACCEL_VISIBLE)
		openm.connect('activate', self.OnOpenO)
		
		# Append to menu
		filemenu.append(openm)

		# Create and append a separator to menu
		sep = gtk.SeparatorMenuItem()
		filemenu.append(sep)

		# Create a item and accelerator
		exit = gtk.ImageMenuItem(gtk.STOCK_QUIT, agr)
		key, mod = gtk.accelerator_parse("<Control>Q")
		exit.add_accelerator("activate", agr, key, 
    	mod, gtk.ACCEL_VISIBLE)

		exit.connect("activate", self.Close)

		# Append to menu
		filemenu.append(exit)

		mb.append(filem)
		
		#Append menu to box
		vbox.pack_start(mb, False, False, 5)	
	
		# Create a horizontal separator and append
		hseparator1 = gtk.HSeparator()
		vbox.pack_start(hseparator1, False, False, 0)

		# Create a box (horizontal)
		hbox1 = gtk.HBox(True, 10)		

		# Create a combobox, connect it to a function and append to box
		self.combobox1 = gtk.combo_box_new_text()	
		self.combobox1.connect('changed', self.OnChangeCB, 1)	

		hbox1.pack_start(self.combobox1, False, False, 0)

		# Create a combobox, connect it to a function and append to box
		self.combobox2 = gtk.combo_box_new_text()	
		self.combobox2.connect('changed', self.OnChangeCB, 2)	

		hbox1.pack_start(self.combobox2, False, False, 0)
		
		# Append box to main box
		vbox.pack_start(hbox1, False, False, 0)

		# Create a horizontal separator and append
		hseparator2 = gtk.HSeparator()
		vbox.pack_start(hseparator2, False, False, 0)

		# Create a box (horizontal)
		hbox2 = gtk.HBox(True, 10)		

		# Create a scrolled window, append to box and show
		scrolled_window1 = gtk.ScrolledWindow()
		hbox2.pack_start(scrolled_window1, True, True, 0)		
		scrolled_window1.show()
		
		# Create a table
		self.table1 = gtk.Table(2, 2, True)

		# Create, set, and show a image
		self.image1 = gtk.Image()
		self.image1.set_from_file("img.png")	
		self.image1.show()

		# Append image to table
		self.table1.attach(self.image1, 0, 2, 0, 2)

		# Append and show table
		scrolled_window1.add_with_viewport(self.table1)
		self.table1.show()

		# Create a scrolled window, append to box and show
		scrolled_window2 = gtk.ScrolledWindow()
		hbox2.pack_start(scrolled_window2, True, True, 0)		
		scrolled_window2.show()
		
		# Create a table
		self.table2 = gtk.Table(2, 2, False)

		# Create, set and show a image
		self.image2 = gtk.Image()
		self.image2.set_from_file("img.png")	
		self.image2.show()
		
		# Append image to table
		self.table2.attach(self.image2, 0, 2, 0, 2)

		# Append and show table
		scrolled_window2.add_with_viewport(self.table2)
		self.table2.show()

		# Append box to main box
		vbox.pack_start(hbox2, True, True, 0)

		# Create and append a horizontal separator
		hseparator3 = gtk.HSeparator()		
		vbox.pack_start(hseparator3, False, False, 0)

		# Create a box (horizontal)
		hbox3 = gtk.HBox(False, 10)

		# Create and append two buttons
		button1 = gtk.Button(stock=gtk.STOCK_APPLY)
		button2 = gtk.Button(stock=gtk.STOCK_CANCEL)

		hbox3.pack_end(button1, False, False, 0)		
		hbox3.pack_end(button2, False, False, 0)

		button1.connect("clicked", self.OnButton1)
		button2.connect("clicked", self.OnButton2)
		
		# Append box to main box
		vbox.pack_start(hbox3, False, False, 0)

		# Add main box to window
		self.add(vbox)

		# Connect delete event to Close function
		self.connect("delete-event", self.Close)

	def Close(self, b, c):
		""" Clean tempdirs and move final apk to target
		
		Args:
		    anything
		    
		Return:
		    anything
		"""
		
		# Clean all tempdirs
		if os.path.exists(tempdir+'/apkmodder-theme'):
			shutil.rmtree(tempdir+'/apkmodder-theme')
		if os.path.exists(tempdir+'/apkmodder-mod'):
			shutil.rmtree(tempdir+'/apkmodder-mod')
		if os.path.exists(tempdir+'/apkmodder-match'):
			shutil.rmtree(tempdir+'/apkmodder-match')
		
		# Check if has been created a modded apk
		if hasattr(self, 'output_apk'):
		  
			# Close zip
			self.output_apk.close()
			
			# Remove actual mod apk
			os.remove(self.pathi)
			
			#Substituite old apk (deleted) with the modded apk
			shutil.move(tempdir+'/output.apk', self.pathi)
		
		# Destory all and close program
		gtk.main_quit()

	def OnChangeCB(self, combobox, number):
		""" When ComboBox is modified set up new image
		
		Args:
		    self, combobox, number (mod-theme)
		    
		Return:
		    anything
		"""
		
		# Check if is first using, if yes break
		if not hasattr(self, 'firstI') and number == 1:
			self.firstI=True
			return
			
		if not hasattr(self, 'firstO') and number == 2:
			self.firstO=True
			return
			
		# Get selected text
		value=combobox.get_active_text()
		
		if number == 1:
			# Remove all images
			for imageob in self.liimageob:
				self.table1.remove(imageob)
		
			# Remove all checkbuttons
			for checkbutton in self.lcheckbuttonob:
				self.table1.remove(checkbutton)
			
			# Create a list of image to pass to function Draw
			limage = GetImageToDraw(self.diimagedir, value, 1)
				
			# Draw image to table
			self.DrawI(limage)	
					
		elif number == 2:	
			# Remove all images
			for imageob in self.loimageob:
				self.table2.remove(imageob)
				
			# Remove all labels
			for label in self.llabelob:
				self.table2.remove(label)

			# Create a list of image to pass to function Draw
			limage = GetImageToDraw(self.doimagedir, value, 2)
				
			# Draw image to table
			self.DrawO(limage)	
			
	def rtoggled(self, widget):
		""" Create a target
		
		Args:
		    self, widget
		    
		Return:
		    anything
		"""
		#Create target
		if widget.get_active():
			self.target = widget.get_label()


	def OnOpenI(self, a):
		""" Open and prepere the apk for drawing to the table
		
		Args:
		    self
		
		Return:
		    anything
		
		"""
		if self.apki == False:
			
			# Get Apk path
			self.pathi = GetPath() 
			
			# Check if the path exsist, if not exsist break
			if self.pathi == None:
				logger.error('OnOpenI -> Path empty')
				return
			
			# Check if zip is good
			try:
				ztest = zipfile.ZipFile(self.pathi, 'r')
			except zipfile.BadZipfile:
				logger.error('OnOpenI -> Bad zipfile')
				md = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "Bad zipfile")
				md.run()
				md.destroy()
				return
			
			# Create ZipFile object
			self.zinput = zipfile.ZipFile(self.pathi, 'a')
			
			# Create lots variable
			self.apki = True
			self.lidrawable=[]
			self.diimagedir={}
			 			 
			 # Extract the apk to tempdir+/apkmodder-mod
			self.zinput.extractall(tempdir+'/apkmodder-mod') 

			# Get drawables folders names
			self.lidrawable = GetDrawable(1)
			
			# Get corrispondence between drawables folders and files that contain
			self.diimagedir = GetDrawableFiles(self.lidrawable, 1)
			
			# Set combobox
			for text in self.lidrawable:
				SetCombobox(self, 1, text, True)
			
			# Remove the inital image (No Apk Selected)
			self.table1.remove(self.image1)
			
			# Resize the images		
			ResizeToDraw(self.diimagedir)
			
			# Create a list of image to pass to function Draw
			limagestart = GetImageToDraw(self.diimagedir, self.lidrawable[0], 1)
			
			# Draw image to table
			self.DrawI(limagestart)
	
		elif self.apki == True:		
			md = gtk.MessageDialog(self, 
				gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
				gtk.BUTTONS_CLOSE, "File already selected")
			md.run()
			md.destroy()
			
	def OnOpenO(self, a):
		""" Open and prepere the apk for drawing to the table
		
		Args:
		    self
	
		Return:
		    anything
		
		"""
		if self.apko == False:

			# Get Apk path
			self.patho = GetPath()
			
			# Check if the path exsist, if not exsist break
			if self.patho == None:
				return
			
			# Create lots variable
			self.apko = True
			self.zoutput = zipfile.ZipFile(self.patho)
			self.lodrawable=[]
			self.doimagedir={}
			
			# Extract the apk to tempdir+/apkmodder-theme
			self.zoutput.extractall(tempdir+'/apkmodder-theme')

			# Get drawables folders names
			self.lodrawable = GetDrawable(2)
			
			# Get corrispondence between drawables folders and files that contain
			self.doimagedir = GetDrawableFiles(self.lodrawable, 2)
			
			# Set combobox
			for text in self.lodrawable:
				SetCombobox(self, 2, text, True)
			
			# Remove the inital image (No Apk Selected)
			self.table2.remove(self.image2)
			
			# Resize the images		
			ResizeToDraw(self.doimagedir)
			
			# Create a list of image to pass to function Draw
			limagestart = GetImageToDraw(self.doimagedir, self.lodrawable[0], 2)
			
			# Draw image to table
			self.DrawO(limagestart)

		elif self.apko == True:
			md = gtk.MessageDialog(self, 
				gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
				gtk.BUTTONS_CLOSE, "File already selected")
			md.run()
			md.destroy()	

	def DrawI(self, limage):		
		""" Draw a list of image to gtk table
		
		Args:
		    self, list of image
		    
		Return:
		    anything
		"""
		
		# Create 2 variable for create a correct incolunation
		a=0
		b=1
		
		# Create variable for save objects
		self.liimageob = []
		self.lcheckbuttonob = []
		self.diob = {}
		
		for image in limage:
			# Control incolunation
			a=a+1
			if a > 3:
				b=b+2
				a=1
				
			# Create gtk image object, set and show
			self.image1 = gtk.Image()		
			self.image1.set_from_file(image+'resized.png')
			self.image1.show()
			
			# Append image object to dict, table and list
			self.diob[image] = self.image1
			self.table1.attach(self.image1, a-1, a, b-1, b)
			self.liimageob.append(self.image1)
			
			# Create checkbutton object and show
			self.checkbutton1 = gtk.CheckButton(os.path.basename(image)) 
			self.checkbutton1.show()
			
			# Connect checkbutton to Match, attach to table and append to list
			self.checkbutton1.connect('clicked', self.Match, image)
			self.table1.attach(self.checkbutton1, a-1, a, b, b+1)	
			self.lcheckbuttonob.append(self.checkbutton1)

	def DrawO(self, limage):
		""" Draw a list of image to gtk table
		
		Args:
		    self, list of image
		    
		Return:
		    anything
		"""
		
		# Create 2 variable for create a correct incolunation
		a=0
		b=1
		c=-1
		
		# Create variable for save objects
		self.loimageob = []
		self.llabelob = []
		self.doob = {}
		
		for image in limage:
			# Control incolunation
			a=a+1
			c=c+1
			if a > 3:
				b=b+2
				a=1
				
			# Append image object to dict, table and list
			self.image2 = gtk.Image()		
			self.image2.set_from_file(image+'resized.png')
			self.image2.show()
			
			# Append image object to dict, table and list
			self.loimageob.append(self.image2)
			self.doob[image] = self.image2
			self.table2.attach(self.image2, a-1, a, b-1, b)
			
			# Create label object and show
			self.label = gtk.Label(os.path.basename(image))
			self.label.show()
			
			# Append to table and to list
			self.table2.attach(self.label, a-1, a, b, b+1)
			self.llabelob.append(self.label)

	def Match(self, widget, imagen):
	  
		if widget.get_active():
			
			if self.apko is True:
				if not hasattr(self, 'dmatch'):  
					self.dmatch={}
				if not hasattr(self, 'dsize'):
					self.dsize={} 
			
				localdmatch = {}
				localdsize = {}

				for image in self.loimage:
					if os.path.basename(imagen) in image+'resize.png':
						size=GetImageSize(imagen)

						localdmatch[image]=imagen
						localdsize[image]=size
						
				if len(localdmatch) == 1:
					self.dmatch = dict(self.dmatch.items() + localdmatch.items())
					self.dsize = dict(self.dsize.items() + localdsize.items())

				elif len(localdmatch) > 1:
					self.target=''
					self.imagen=imagen
					
					self.choosedialog = gtk.Window(gtk.WINDOW_TOPLEVEL)
					#self.choosedialog.connect("destroy", lambda w: gtk.main_quit())

					self.choosedialog.set_title('Multi-match')
					self.choosedialog.set_border_width(15)

					self.vbox2 = gtk.VBox(True, 10)

					frame = gtk.Frame('Multi Match')
					label2 = gtk.Label('There are '+str(len(localdmatch))+' matches for the selected .png. Select the .png you want port')

					self.vbox2.pack_start(label2, 10)

					first = True
					for key in localdmatch:
						if first:
							group = None
							self.target=key
							first = False
						else:
							group = radio
						radio = gtk.RadioButton(group, key)
						radio.connect('toggled', self.rtoggled)
						self.vbox2.pack_start(radio, True, True, 0)
						radio.show()

					button3 = gtk.Button(stock=gtk.STOCK_OK)
					self.vbox2.pack_end(button3, True, True, 10)
					
					button3.connect('clicked', self.OnButton3, self.choosedialog)
					
					frame.add(self.vbox2)
					self.choosedialog.add(frame)

					self.choosedialog.show_all ()
				elif len(localdmatch) == 0:
					md = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "No match for the selected .png")
					md.run()
					md.destroy()
					widget.set_active(False)
			else:
				md = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "No apk theme selected")
				md.run()
				md.destroy()
				widget.set_active(False)
				
	def OnButton1(self, widget):
		if hasattr(self, 'dmatch') and hasattr(self, 'dsize'):
			for key in self.dsize:
				ob = re.search(tempdir+'/apkmodder-mod/res/(.+)', self.dmatch[key], re.M|re.I)
				
				if not os.path.exists(tempdir+'/apkmodder-match/'+os.path.dirname(ob.group(1))):
					os.makedirs(tempdir+'/apkmodder-match/'+os.path.dirname(ob.group(1)))
					
				os.remove(tempdir+'/apkmodder-mod/res/'+ob.group(1))
				
				subprocess.call(['convert', key, '-resize', str(self.dsize[key][0])+'x'+str(self.dsize[key][1])+'!', tempdir+'/apkmodder-mod/res/'+ob.group(1)])
				
			self.output_apk=zipfile.ZipFile(tempdir+'/output.apk', 'w')
				
			for root, dirs, files in os.walk(tempdir+'/apkmodder-mod'):
			  
				for f in files:
					try: 
						ob = re.match(tempdir+'/apkmodder-mod/(.+)', root, re.M|re.I)
						ob.group(1)
						a = True
					except:
						a = False
					if 'output.apk' in f:
						continue
					if 'resized' in f:
						continue
						
					if a:
						self.output_apk.write(root+'/'+f, ob.group(1)+'/'+f)
					elif not a:
						self.output_apk.write(root+'/'+f, f)

	def OnButton2(self, a):
		self.dmatch={}
		self.dsize={}

	def OnButton3(self, a, window):
		if not self.target == '':
			self.dmatch[self.target]=self.imagen
			self.dsize[self.target]=GetImageSize(self.imagen)
			window.destroy()

win = MyWindow()
win.show_all()
gtk.main()

