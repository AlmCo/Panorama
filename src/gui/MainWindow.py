# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from actions.Report import GuiReportBuilding
from actions.Files import FilesFinder
from common.encodedFiles import *
import logView


try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_Panorama(QtGui.QMainWindow):
	def __init__(self):
		self.logView = logView.logView(self)
		QtGui.QMainWindow.__init__(self)
		self.setupUi(self)
	
	def setupUi(self, Panorama):
		# GUI settings:
		Panorama.setObjectName(_fromUtf8("Panorama"))
		Panorama.resize(445, 440)
		Panorama.setAnimated(False)
		Panorama.setDocumentMode(False)

		# Setting the centralwidget:
		self.centralwidget = QtGui.QWidget(Panorama)
		self.centralwidget.setStyleSheet(_fromUtf8("background-color: rgb(7, 33, 68);"))
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		
		# Set icon
		icon = QtGui.QPixmap()
		icon.loadFromData(iconIco)
		Panorama.setWindowIcon(QtGui.QIcon(icon))
		
		# Logo is decoded from base64:
		logo = QtGui.QPixmap()
		logo.loadFromData(guiLogo)
		self.LogoView = QtGui.QLabel(self.centralwidget)
		self.LogoView.setGeometry(QtCore.QRect(15, 10, 560, 101))
		self.LogoView.setPixmap(logo)

		# Report Button:
		self.ReportGen = QtGui.QPushButton(self.centralwidget)
				#								X 	  Y    W    H
		self.ReportGen.setGeometry(QtCore.QRect(290, 123, 145, 51))
		self.ReportGen.setStyleSheet(_fromUtf8("font: 95 17pt \"Arial\";\n"
												"color: rgb(9, 38, 49);\n"
												"background-color: qlineargradient(spread:pad, x1:0.387, y1:0.926, x2:0.93733, y2:0.119, stop:0 rgba(184, 184, 184, 255), stop:1 rgba(255, 255, 255, 255));\n"
												"border-radius: 15px;\n"
												"border:2px solid rgb(190, 190, 190); "))
		self.ReportGen.setObjectName(_fromUtf8("ReportGen"))
		self.ReportGen.clicked.connect(self.startReport)


		# Media file scanning button:
		self.FindFiles = QtGui.QPushButton(self.centralwidget)
		self.FindFiles.setGeometry(QtCore.QRect(290, 190, 145, 51))		
		self.FindFiles.setStyleSheet(_fromUtf8("font: 95 17pt \"Arial\";\n"
													"color: rgb(9, 38, 49);\n"
													"background-color: qlineargradient(spread:pad, x1:0.387, y1:0.926, x2:0.93733, y2:0.119, stop:0 rgba(184, 184, 184, 255), stop:1 rgba(255, 255, 255, 255));\n"
													"border-radius: 15px;\n"
													"border:2px solid rgb(190, 190, 190); "))
		self.FindFiles.setObjectName(_fromUtf8("FindFiles"))
		self.FindFiles.clicked.connect(self.startFindFiles)


		# Hibernate button:
		self.Hibernate = QtGui.QPushButton(self.centralwidget)
		self.Hibernate.setGeometry(QtCore.QRect(290, 260, 145, 51))		
		self.Hibernate.setStyleSheet(_fromUtf8("font: 75 13.5pt \"Arial\";\n"
													"color: rgb(9, 38, 49);\n"
													"background-color: qlineargradient(spread:pad, x1:0.387, y1:0.926, x2:0.93733, y2:0.119, stop:0 rgba(184, 184, 184, 255), stop:1 rgba(255, 255, 255, 255));\n"
													"border-radius: 15px;\n"
													"border:2px solid rgb(190, 190, 190); "))
		self.Hibernate.setObjectName(_fromUtf8("Hibernate"))
		self.Hibernate.clicked.connect(self.startHibernate)


		# Close and Delete button:
		self.CloseAndDelete = QtGui.QPushButton(self.centralwidget)
		self.CloseAndDelete.setGeometry(QtCore.QRect(290, 330, 145, 51))
		self.CloseAndDelete.setStyleSheet(_fromUtf8("font: 75 13.5pt \"Arial\";\n"
													"color: rgb(9, 38, 49);\n"
													"background-color: qlineargradient(spread:pad, x1:0.387, y1:0.926, x2:0.93733, y2:0.119, stop:0 rgba(184, 184, 184, 255), stop:1 rgba(255, 255, 255, 255));\n"
													"border-radius: 15px;\n"
													"border:2px solid rgb(190, 190, 190); "))
		self.CloseAndDelete.setObjectName(_fromUtf8("CloseAndDelete"))
		self.CloseAndDelete.clicked.connect(self.closeAndDelete)


		# About button:
		self.AboutButton = QtGui.QPushButton(self.centralwidget)
		self.AboutButton.setGeometry(QtCore.QRect(365, 400, 70, 30))
		self.AboutButton.setStyleSheet(_fromUtf8("font: 75 14pt \"Arial\";\n"
													"color: rgb(9, 38, 49);\n"
													"background-color: qlineargradient(spread:pad, x1:0.387, y1:0.926, x2:0.93733, y2:0.119, stop:0 rgba(184, 184, 184, 255), stop:1 rgba(255, 255, 255, 255));\n"
													"border-radius: 15px;\n"
													"border:2px solid rgb(190, 190, 190); "))
		self.AboutButton.setObjectName(_fromUtf8("AboutButton"))
		self.AboutButton.clicked.connect(lambda: self.showMessageBox("About","Panorama\n\nSupports Windows XP SP2 and up.\n\nwww.github.com/AlmCo/Panorama\nalmogcn@gmail.com"))


		# Just close button:
		self.CloseButton = QtGui.QPushButton(self.centralwidget)
		self.CloseButton.setGeometry(QtCore.QRect(290, 400, 70, 30))
		self.CloseButton.setStyleSheet(_fromUtf8("font: 75 14pt \"Arial\";\n"
													"color: rgb(9, 38, 49);\n"
													"background-color: qlineargradient(spread:pad, x1:0.387, y1:0.926, x2:0.93733, y2:0.119, stop:0 rgba(184, 184, 184, 255), stop:1 rgba(255, 255, 255, 255));\n"
													"border-radius: 15px;\n"
													"border:2px solid rgb(190, 190, 190); "))
		self.CloseButton.setObjectName(_fromUtf8("CloseButton"))
		self.CloseButton.clicked.connect(self.closeGui)


		# Log View box:
		self.logBox = QtGui.QTextBrowser(self.centralwidget)
		self.logBox.setGeometry(QtCore.QRect(10, 120, 270, 310))
		self.logBox.setStyleSheet(_fromUtf8("padding-left: 5px;\n"
											"padding-right: 5px;\n"
											"font: 75 12pt \"Arial\";\n"
											"color: rgb(9, 38, 49);\n"
											"border-radius: 5px;\n"
											"border:2px solid rgb(190, 190, 190);\n"
											"background-color: rgb(230, 230, 230);\n"))
		self.logBox.verticalScrollBar().setStyleSheet(_fromUtf8("color: rgb(230, 230, 230);\nheight: 0px;"))
		self.logBox.verticalScrollBar().setHidden(1)


		Panorama.setCentralWidget(self.centralwidget) # Setting the main widget
		self.retranslateUi(Panorama) # Getting names for the buttons
		QtCore.QMetaObject.connectSlotsByName(Panorama)


	def update(self):
		# Using from another files to update the logView
		self.retranslateUi(self)
		self.logBox.verticalScrollBar().setValue(self.logBox.verticalScrollBar().maximum())
		QtCore.QCoreApplication.processEvents()

	def retranslateUi(self, Panorama):
		# Translate the name for each attribute:
		Panorama.setWindowTitle(_translate("Panorama", "Panorama", None))
		self.ReportGen.setText(_translate("Panorama", "Report", None))
		self.FindFiles.setText(_translate("Panorama", "Files Finder", None))
		self.Hibernate.setText(_translate("Panorama", "Hibernate", None))
		self.CloseAndDelete.setText(_translate("Panorama", "Close and Delete", None))
		self.AboutButton.setText(_translate("Panorama", "About", None))
		self.CloseButton.setText(_translate("Panorama", "Close", None))
		self.logBox.setHtml(_translate("Panorama", self.logView.log, None)) # self.logView.log is the variable that holds the HTML	

	def showMessageBox(self, title, message):
		# Creating popup message
		msg = QtGui.QMessageBox()
		msg.setIcon(QtGui.QMessageBox.Information)
		# Set icon
		icon = QtGui.QPixmap()
		icon.loadFromData(iconIco)
		msg.setWindowIcon(QtGui.QIcon(icon))
		# Creating the popup
		msg.setText(message.decode('utf-8'))
		msg.setWindowTitle(title.decode('utf-8'))
		msg.setStandardButtons(QtGui.QMessageBox.Ok)
		retval = msg.exec_()


	def startReport(self):
		# Calling to ReportBuilding to generate the report and open the webpage
		GuiReportBuilding(self)


	def startFindFiles(self):
		# No time to explain:
		FilesFinder(self)

	def startHibernate(self):
		popen("%windir%\\system32\\powercfg.exe /h on")
		popen("%windir%\\system32\\shutdown.exe /h")
		popen("%windir%\\system32\\rundll32.exe powrprof.dll,SetSuspendState")

	def closeGui(self):
		# Closing the app
		QtCore.QCoreApplication.instance().quit()

	def closeAndDelete(self):
		# Close the app, Eject the cd-rom and delete the dir from Temp folder
		rmPanoramaDir()
		self.closeGui()
