# -*- coding: utf-8 -*-

from os import popen, listdir
from os.path import isdir, isfile
from lib.Registry import *

SystemRoot = str(readName(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",'SystemRoot'))
TEMP = str(readName(r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",'TEMP'))

appdata = popen("echo %appdata%").read().split("\n")[0]

sysTempFolder = TEMP.replace("%SystemRoot%",SystemRoot)
PanoramaDir = sysTempFolder+"\Panorama"

# WEB:
PanoramaReportPage = PanoramaDir+"\Panorama.html"
PanoramaFilesPage = PanoramaDir+"\FilesPanorama.html"
WebLogo = PanoramaDir+"\logo.png"

#TXT:
txtPanoramaReportPage = PanoramaDir+"\Panorama.txt"
txtPanoramaFilesPage = PanoramaDir+"\FilesPanorama.txt"

if not isdir(PanoramaDir):
	# if Panorama dir not exist - create the dir
	popen("mkdir "+PanoramaDir)



def rmPanoramaDir():
	popen("rmdir /s /q "+PanoramaDir)