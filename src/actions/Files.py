# -*- coding: utf-8 -*-

from os import walk

from utils.HTML import *

wantedFiles = {"ppt":"content",
				"pptx":"content", 
				"doc":"content",
				"docx":"content", 
				"pdf":"content", 
				"xslx":"content", 
				"avi":"video", 
				"wmv":"video", 
				"mp4":"video", 
				"jpg":"photo",
				"jpeg":"photo",
				"gif":"photo",
				"png":"photo"}

class FilesFinder():
	def __init__(self, Ui_Panorama):
		self.contentFiles = []
		self.videoFiles = []
		self.photoFiles = []
		Ui_Panorama.logView.write("Start scanning")
		Ui_Panorama.logView.writeColor("Scanning...", "grey")
		Ui_Panorama.logView.write("<b>May take few minutes</b>")

		Ui_Panorama.logView.write("Scan USERS folder..")

		self.scan("c:\users")
		self.scan("c:\documents and settings")

		Ui_Panorama.logView.write("Writing resules...")
		fileslist = FilesList(self.contentFiles, self.photoFiles, self.videoFiles)
		Ui_Panorama.logView.writeColor("Finished, Opens the report", "green")
		fileslist.openReport()
		Ui_Panorama.logView.write("")



	def scan(self, scanPath):
		for root, dirs, files in walk(scanPath):
			for filename in files:
				try:
					if "." in filename and "appdata" not in root.lower():
						name = root+"\\"+filename
						# print name
						extension = name.rsplit(".",1)[1]
						if extension in wantedFiles:
							self.addPath(extension, name)
				except:
					pass

	def addPath(self, ext, path):
		if wantedFiles[ext] == "content":
			self.contentFiles.append(path.decode('iso8859_8'))

		elif wantedFiles[ext] == "video":
			self.videoFiles.append(path.decode('iso8859_8'))

		elif wantedFiles[ext] == "photo":
			self.photoFiles.append(path.decode('iso8859_8'))