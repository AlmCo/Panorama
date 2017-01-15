# -*- coding: utf-8 -*-

# Panorama
# https://github.com/AlmCo/Panorama
# copyright: Almog Cohen <almogcn@gmail.com>

from sys import argv, exit
from PyQt4.QtGui import QApplication

from gui.MainWindow import Ui_Panorama
from actions.Report import TxtReportBuilding

helpScreen = """
 Panorama - Fast incident overview
 ----
	Double click or no more arguments to run with GUI
	Run with argument '-c' to run without GUI, TXT file is default output.

	http://github.com/AlmCo/Panorama
	"""

if __name__ == "__main__":

	if len(argv) > 1:
		if argv[1] == "-c":
			TxtReportBuilding()
		elif argv[1] == "-h":
			print helpScreen
		else:
			print "Try -h"

	else: # GUI:
		app = QApplication(argv)

		Panorama = Ui_Panorama()
		Panorama.show()

		exit(app.exec_())