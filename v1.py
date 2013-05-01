#!/usr/bin/python

#  
#  Welcome to MM7 Android Application Modder
#

print('')
print('APK MODDER')
print('')

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
try:
	import re
except:
	print("FATAL : Can't import re")
	sys.exit(0)
try:
	import subprocess
except:
	print("FATAL : Can't import subprocess")
	sys.exit(0)


tempdir = tempfile.gettempdir()

def GetImageSize(path):
	image = Image.open(path)
	x, y = image.size
	return(x, y)

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

		openi = gtk.MenuItem(label = 'Open mod apk')
		key, mod = gtk.accelerator_parse("<Control>I")
		openi.add_accelerator("activate", agr, key, 
    	mod, gtk.ACCEL_VISIBLE)
		openi.connect('activate', self.OnOpen, 0)

		filemenu.append(openi)

		openm = gtk.MenuItem(label = 'Open theme apk')
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
		self.image1.set_from_file("img.png")	
		self.image1.show()

		self.table1.attach(self.image1, 0, 2, 0, 2)

		scrolled_window1.add_with_viewport(self.table1)
		self.table1.show()

		scrolled_window2 = gtk.ScrolledWindow()
		hbox2.pack_start(scrolled_window2, True, True, 0)		
		scrolled_window2.show()
		
		self.table2 = gtk.Table(2, 2, False)

		self.image2 = gtk.Image()
		self.image2.set_from_file("img.png")	
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

		button1.connect("clicked", self.OnButton1)
		button2.connect("clicked", self.OnButton2)
		
		vbox.pack_start(hbox3, False, False, 0)

		self.add(vbox)

		self.connect("delete-event", self.Close)

	def Close(self, b, c):
		if os.path.exists(tempdir+'/apkmodder-theme'):
			shutil.rmtree(tempdir+'/apkmodder-theme')
		if os.path.exists(tempdir+'/apkmodder-mod'):
			shutil.rmtree(tempdir+'/apkmodder-mod')
		if os.path.exists(tempdir+'/apkmodder-match'):
			shutil.rmtree(tempdir+'/apkmodder-match')
		if hasattr(self, 'output_apk'):
			self.output_apk.close()
			os.rename(tempdir+'output.apk', '/home/marco/output.apk')
		gtk.main_quit()

	def changed_cbI(self, combobox):
		model = combobox.get_model()	
		index = combobox.get_active()
		for imageob in self.liimageob:
			self.table1.remove(imageob)
		for checkbutton in self.lcheckbuttonob:
			self.table1.remove(checkbutton)
		if index:
			limage=self.diimagedir[tempdir+'/apkmodder-mod/res/'+model[index][0]]
			lpass=[]
			for image in limage:
				lpass.append(tempdir+'/apkmodder-mod/res/'+model[index][0]+'/'+image)
			lpass.sort()
		#if index:
		#	ldirfname = GetZipDrawableFileName(self.liimage, model[index][0])
		#	ldirfname.sort()
			self.DrawI(lpass)	

	def changed_cbO(self, combobox):
		model = combobox.get_model()	
		index = combobox.get_active()
		for imageob in self.loimageob:
			self.table2.remove(imageob)
		for label in self.llabelob:
			self.table2.remove(label)
		if index:
			
			limage=self.doimagedir[tempdir+'/apkmodder-theme/res/'+model[index][0]]
			lpass=[]
			for image in limage:
				lpass.append(tempdir+'/apkmodder-theme/res/'+model[index][0]+'/'+image)
			lpass.sort()
			#ldirfname = GetZipDrawableFileName(self.loimage, model[index][0])
			#ldirfname.sort()
			self.DrawO(lpass)
			
	def rtoggled(self, widget):
		if widget.get_active():
			self.target = widget.get_label()


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
			self.zinput = zipfile.ZipFile(self.pathi, 'a')
			self.lidir=[]
			self.lifile=[]
			self.liimage=[]
			self.lidrawable=[]
			self.diimagedir={}
			
			self.zinput.extractall(tempdir+'/apkmodder-mod')

			for root, dirs, files in os.walk(tempdir+'/apkmodder-mod/res'):
				if root == tempdir+'/apkmodder-mod/res':
					for rdir in dirs:
						if re.search(r'drawable-\w+', rdir, re.M|re.I):
							self.lidrawable.append(rdir)
							#self.dimagedir[tempdir+'/apkmoddertmp/res/'+rdir]='Void'
				for d in self.lidrawable:
					if root == tempdir+'/apkmodder-mod/res/'+d:
						self.diimagedir[root] = files
				#self.dimagedir[root] = files
				#self.lidir.append(dirs)
				self.lifile = self.lifile+files
			
			for di in self.lidrawable:
				self.combobox1.append_text(di)
				#self.lidrawable.append(di)
			
			#self.lidrawable = GetZipDrawableName(self.lifile)			
			#for dirdrawable in self.lidrawable:
			#	self.combobox1.append_text(dirdrawable)
			self.table1.remove(self.image1)
			#self.liimage = GetZipImageName(self.lifile)
			for key in self.diimagedir:
				for value in self.diimagedir[key]:
					if os.path.splitext(value)[1] == '.png':
						self.liimage.append(key+'/'+value)
			#for f in self.lifile:
			#	if os.path.splitext(f)[1] == '.png':
			#		self.liimage.append(f)
					
			#for key in self.diimagedir:
			#	for value in self.diimagedir[key]:
					#subprocess.call(['convert', tempdir+'/apkmoddertmp/'+image, '-resize', '50x50!', tempdir+'/apkmoddertmp/'+image+'resized.png'])
			for image in self.liimage:
				subprocess.call(['convert',image, '-resize', '50x50', image+'resized.png'])	
			
			limagestart=[]
			for value in self.diimagedir[tempdir+'/apkmodder-mod/res/'+self.lidrawable[0]]:
				limagestart.append(tempdir+'/apkmodder-mod/res/'+self.lidrawable[0]+'/'+value)
				limagestart.sort()
				#im1 = Image.open(tempdir+'/apkmoddertmp/'+image)
				#im2 = im1.thumbnail(dim, Image.NEAREST)	
				#im2.save(tempdir+'/apkmoddertmp/'+image+'resized.png')
			#print(self.lidrawable)
			#Extract(self.zinput)
			#Resize(self.liimage)
			#lidirfname = GetZipDrawableFileName(self.liimage, self.lidrawable[0])
			self.DrawI(limagestart)

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
			self.lodir=[]
			self.lofile=[]
			self.loimage=[]
			self.lodrawable=[]
			self.doimagedir={}
			
			self.zoutput.extractall(tempdir+'/apkmodder-theme')

			for root, dirs, files in os.walk(tempdir+'/apkmodder-theme/res'):
				if (root == tempdir+'/apkmodder-theme/res'):
					for rdir in dirs:
						if re.search(r'drawable-\w+', rdir, re.M|re.I):
							self.lodrawable.append(rdir)
							#self.dimagedir[tempdir+'/apkmoddertmp/res/'+rdir]='Void'
				for d in self.lodrawable:
					if root == tempdir+'/apkmodder-theme/res/'+d:
						self.doimagedir[root] = files
				#self.doimagedir[root] = files
				#self.lidir.append(dirs)
				self.lofile = self.lofile+files
			
			for di in self.lodrawable:
				self.combobox2.append_text(di)
				#self.lidrawable.append(di)
			
			#self.lidrawable = GetZipDrawableName(self.lifile)			
			#for dirdrawable in self.lidrawable:
			#	self.combobox1.append_text(dirdrawable)
			self.table2.remove(self.image2)
			#self.liimage = GetZipImageName(self.lifile)
			for key in self.doimagedir:
				for value in self.doimagedir[key]:
					if os.path.splitext(value)[1] == '.png':
						self.loimage.append(key+'/'+value)
			#for f in self.lifile:
			#	if os.path.splitext(f)[1] == '.png':
			#		self.liimage.append(f)
					
			#for key in self.doimagedir:
			#	for value in self.doimagedir[key]:
					#subprocess.call(['convert', tempdir+'/apkmoddertmp/'+image, '-resize', '50x50!',tempdir+'/apkmoddertmp/'+image+'resized.png'])
			for image in self.loimage:
				subprocess.call(['convert', image, '-resize', '50x50', image+'resized.png'])	
			
			limagestart=[]
			for value in self.doimagedir[tempdir+'/apkmodder-theme/res/'+self.lodrawable[0]]:
				limagestart.append(tempdir+'/apkmodder-theme/res/'+self.lodrawable[0]+'/'+value)
				limagestart.sort()
				#im1 = Image.open(tempdir+'/apkmoddertmp/'+image)
				#im2 = im1.thumbnail(dim, Image.NEAREST)	
				#im2.save(tempdir+'/apkmoddertmp/'+image+'resized.png')
			#print(self.lidrawable)
			#Extract(self.zinput)
			#Resize(self.liimage)
			#lidirfname = GetZipDrawableFileName(self.liimage, self.lidrawable[0])
			self.DrawO(limagestart)

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
			self.image1.set_from_file(image+'resized.png')
			self.image1.show()
			self.diob[image] = self.image1
			self.table1.attach(self.image1, a-1, a, b-1, b)
			self.liimageob.append(self.image1)
			self.checkbutton1 = gtk.CheckButton(os.path.basename(image)) 
			self.checkbutton1.show()
			self.checkbutton1.connect('clicked', self.Match, image)
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
			self.image2.set_from_file(image+'resized.png')
			self.image2.show()
			self.loimageob.append(self.image2)
			self.doob[image] = self.image2
			self.table2.attach(self.image2, a-1, a, b-1, b)
			self.label = gtk.Label(os.path.basename(image))
			self.label.show()
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
						#print(image)
						#print(imagen)
						#print(size)
						localdmatch[image]=imagen
						localdsize[image]=size

						print('Match complete')
						
				if len(localdmatch) == 1:
					self.dmatch = dict(self.dmatch.items() + localdmatch.items())
					self.dsize = dict(self.dsize.items() + localdsize.items())
				#if mok is False:
				 # print('False')
				#if any(imagebn in s for s in self.loimage):		
					#print(GetImageSize(self.loimageob)[0])
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
							first = False
						else:
							group = radio
						radio = gtk.RadioButton(group, key)
						radio.connect('toggled', self.rtoggled)
						self.vbox2.pack_start(radio, True, True, 0)
						radio.show()

					button3 = gtk.Button('Confirm')
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
				
		print(self.dmatch, self.dsize)
				
	def OnButton1(self, widget):
		if self.dmatch and self.dsize:
			for key in self.dsize:
				ob = re.search(tempdir+'/apkmodder-mod/res/(.+)', self.dmatch[key], re.M|re.I)
				#print(self.dmatch[key])
				#print(ob.group(1))
				#print(key)
				
				if not os.path.exists(tempdir+'/apkmodder-match/'+os.path.dirname(ob.group(1))):
					os.makedirs(tempdir+'/apkmodder-match/'+os.path.dirname(ob.group(1)))
					
				os.remove(tempdir+'/apkmodder-mod/res/'+ob.group(1))
				
				subprocess.call(['convert', key, '-resize', str(self.dsize[key][0])+'x'+str(self.dsize[key][1]), tempdir+'/apkmodder-mod/res/'+ob.group(1)])
				
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
					
					print(f)
					
					try:
						print(ob.group(1))
					except:
						print('no')
						
					if a:
						self.output_apk.write(root+'/'+f, ob.group(1)+'/'+f)
					elif not a:
						self.output_apk.write(root+'/'+f, f)
						
			#self.zinput.write(tempdir+'/apkmodder-match/'+ob.group(1), 'res/'+ob.group(1))
			#self.zinput.close()
	def OnButton2(self, a):
		self.dmatch={}
		self.dsize={}

	def OnButton3(self, a, window):
		if not self.target == '':
			self.dmatch[self.target]=self.imagen
			self.dsize[self.target]=GetImageSize(self.imagen)
			window.destroy()
			
			print(self.dmatch, self.dsize)

#zz = zipfile.ZipFile('/home/marco/workspace/Nfc.zip', 'a')
#lfile = GetZipFileName(zz)
#ldrawable = GetZipDrawableName(lfile)
#ZipWrite(zz, '/home/marco/workspace/img.png', 'xd')
#zz.close()

win = MyWindow()
win.show_all()
gtk.main()

