# -*- coding: utf-8 -*-

from utils.forensic import forensic
from utils.HTML import *
from utils.TXT import *

class TxtReportBuilding():
	def __init__(self):
		print "Start generate report"
		
		print "OS..."
		forensic.fOS()
		forensic.fSerialNumber()

		print "Firewall..."
		forensic.fFirewall()

		print "Hotfixes..."
		forensic.fHotfixs()

		print "McAfee..."
		forensic.fMcAfee()

		print "USB..."
		forensic.fUSB()

		print "Network cards..."
		forensic.fNetworkCards()

		print "Users..."
		forensic.fUsers()

		print "Installed softwares..."
		forensic.fSoftwareList()

		print "IPs and MACs..."
		forensic.fIPs()
		forensic.fMACs()

		print "Processes..."
		forensic.fProcesses()

		print "Commands on startup..."
		forensic.fCommandsOnStartup()

		print "Netstat..."
		forensic.fNetStat()

		print "Tasks..."
		forensic.fTasks()

		print "Hosts file..."
		forensic.fHosts()

		print "Recent used files..."
		forensic.fRecent()

		if len(forensic.IPs) != 0:
			# If never was connected to network, it's westing time:
			print "ARP Table..."
			forensic.fArpTable()

			print "Net view..."
			forensic.fLocalNetworkMachines()
		else:
			pass

		print "Writing results..."
		report = TextReport(forensic)

		print "\n\nFinished. Output:"
		print txtPanoramaReportPage


class GuiReportBuilding():
	def __init__(self, Ui_Panorama):
		Ui_Panorama.logView.write("Generate report")
		Ui_Panorama.logView.writeColor("Exporting data...", "grey")

		Ui_Panorama.logView.write("Basic OS details..")
		forensic.fOS() # This function fills up the OS dict
		Ui_Panorama.logView.write("<b>Hostname:</b> "+forensic.hostname+"<br>"
								 "<b>OS:</b> "+forensic.OS["ProductName"]+" "+forensic.OS["SP"])
		
		forensic.fSerialNumber() # This function fills up the Serial number variable
		if forensic.serialnumber == "000000":
			Ui_Panorama.logView.writeColor("Can't export serial number","red")

		Ui_Panorama.logView.write("Firewall..")
		forensic.fFirewall()

		Ui_Panorama.logView.write("Hotfixes..")
		forensic.fHotfixs() # This function fills up the installedHotfixes dict
		if forensic.installedHotfixes["Sum"] == -1:
			Ui_Panorama.logView.writeColor("Can't read hotfixes","red")
		
		Ui_Panorama.logView.write("McAfee..")
		forensic.fMcAfee()

		Ui_Panorama.logView.write("USB...")
		forensic.fUSB()

		Ui_Panorama.logView.write("Network cards...")
		forensic.fNetworkCards()

		Ui_Panorama.logView.write("Users...")
		forensic.fUsers()

		Ui_Panorama.logView.write("Softwares...")
		forensic.fSoftwareList()
		
		Ui_Panorama.logView.write("IP Address...")
		forensic.fIPs()

		Ui_Panorama.logView.write("MAC Address...")
		forensic.fMACs()

		Ui_Panorama.logView.write("Processes list...")
		forensic.fProcesses()

		Ui_Panorama.logView.write("Startup commands...")
		forensic.fCommandsOnStartup()

		Ui_Panorama.logView.write("Netstat...")
		forensic.fNetStat()

		Ui_Panorama.logView.write("Task shoulder...")
		forensic.fTasks()

		Ui_Panorama.logView.write("Hosts file...")
		forensic.fHosts()

		Ui_Panorama.logView.write("Recent files...")
		forensic.fRecent()

		if len(forensic.IPs) != 0:
			# If never was connected to network, it's westing time:
			Ui_Panorama.logView.write("ARP Table...")
			forensic.fArpTable()

			Ui_Panorama.logView.write("Net View...")
			forensic.fLocalNetworkMachines()
		else:
			Ui_Panorama.logView.writeColor("Skipped ARP Table and 'Net View'","grey")


		Ui_Panorama.logView.writeColor("Writing results...","grey")

		report = HTMLReport(forensic)
		
		Ui_Panorama.logView.writeColor("Finished, Opens the report", "green")
		
		Ui_Panorama.logView.write("")

		report.openReport()
