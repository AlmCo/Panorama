from distutils.core import setup
import py2exe
from Tkinter import *
 
setup(
	name = 'Panorama',
	pulisher='Almog Cohen',
	description = 'Fast incident overview',
	version = '1.0',
	options = {'py2exe':{'bundle_files': 1, "includes":["Tkinter"], "dll_excludes": ["msvcr90.dll","msvcp90.dll","msvcm90.dll","tcl85.dll","tk85.dll","mfc90.dll","mfc90u.dll","mfcm90.dll","mfcm90u.dll"]}},
	data_files = [("Microsoft.VC90.CRT.manifest"),("Microsoft.VC90.MFC.manifest")],
	console = [{'script':'Panorama.py', "icon_resources": [(1,"sources/panorama.ico")]}],
	zipfile = None,
)