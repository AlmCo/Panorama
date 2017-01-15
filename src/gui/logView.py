# -*- coding: utf-8 -*-

class logView():
    def __init__(self, Ui_Panorama):
        self.log = '<html xmlns="http://www.w3.org/1999/xhtml"><center><b>Panorama</b><br>Fast incident overview'
        self.Ui_Panorama = Ui_Panorama

    def read(self):
        return self.log

    def write(self, string):
    	self.log += "<br>"+string
    	self.Ui_Panorama.update()

    def writeColor(self, string, color):
    	self.log += "<br><font color="+color+">"+string+"</font>"
    	self.Ui_Panorama.update()
    
    def addTextToLogView(self,AddThis): 
    	print self.log