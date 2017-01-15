# -*- coding: utf-8 -*-
import sys
from os import startfile
from os.path import getctime
from datetime import datetime

from common.paths import *

reload(sys)
sys.setdefaultencoding("utf-8")

def timestamp2date(timestamp, hour):
	mydate = datetime.fromtimestamp(int(timestamp))
	if hour == 1:
		return mydate.strftime("%H:%M %d-%m-%Y")
	else:
		return mydate.strftime("%d-%m-%Y")


class TextReport:
	def __init__(self, forensics):
		self.forensics = forensics
		self.Panorama = open(txtPanoramaReportPage, 'w')
		self.writeHeader()
		self.write("Report created: "+str(datetime.now())+"\n")
		self.writeOSDetails()
		self.writeOS()
		self.writeNetwork()
		self.writeSecurity()
		self.writeUSB()
		self.closeReportFile()

	def write(self, string, line=1):
		self.Panorama.write("\t"+string+"\n")

	def writeContent(self, string):
		self.Panorama.write(string+"\n")

	def writeTitle(self, title):
		self.Panorama.write("\n\n"+title+':\n')
	
	def writeHeader(self):
		header = """--Panorama--\nFast incident overview\n\n
Contact: almogcn@gmail.com
Offical page: https://github.com/AlmCo/Panorama\n\n
===================================================\n\n"""
		self.writeContent(header)

	def writeOSDetails(self):
		self.write("Hostname: "+self.forensics.hostname)
		self.write("Serial number: "+self.forensics.serialnumber)
		self.write("OS: "+self.forensics.OS["ProductName"]+" "+self.forensics.OS["SP"]+" "+self.forensics.OS["Bit"])
		self.write("OS Install date: "+self.forensics.OS["InstallDate"])
		self.write("Num of hotfixes: "+str(self.forensics.installedHotfixes["Sum"]))
		self.write("Firewall status: "+(self.forensics.Firewall["Status"]))
	
	def writeOS(self):
		self.writeTitle("Users")
		for user in self.forensics.Users:
			if user not in ["Guest", "DefaultAccount"]:
				self.write(user)
				for value in self.forensics.Users[user]:
					self.write("\t"+(value)+": "+(str(self.forensics.Users[user][value])))
				self.write(" ")


		self.writeTitle("Commands on startup")
		if len(self.forensics.CommandsOnStartup) != 0:
			for command,active in self.forensics.CommandsOnStartup.iteritems():
				try:
					self.write(command+" | active: "+str(active))
				except:
					print "ERROR: 6349"
					print command
		else:
			self.write("Empty")


		self.writeTitle("Task Shoulder")
		if len(self.forensics.Tasks) != 0:
			for task in self.forensics.Tasks:
				self.write(task["TaskName"]+" | NextRun: "+task["Next Run Time"]+" | Status: "+task["Status"])
		else:
			self.write("Empty")


		self.writeTitle("Installed softwares")
		if len(self.forensics.SoftwareList) != 0:
			for software in self.forensics.SoftwareList:
				self.write(software)
		else:
			self.write('Empty')


		self.writeTitle("Recently used files")
		if len(self.forensics.Recent) != 0:
			for each in self.forensics.Recent:
				self.write(each)
		else:
			self.write('Empty')


		self.writeTitle("Active processes")
		if len(self.forensics.Processes) != 0:
			for pid,name in self.forensics.Processes.iteritems():
				if name.strip() not in ["System", "System Idle Process"]:
					if str(self.forensics.Netstat).find(str(name+"', 'PID': '"+str(pid))) == -1:
						self.write(name+" | PID: "+str(pid)+" | Communicating: No")
					else:
						self.write(name+" | PID: "+str(pid)+" | Communicating: Yes")
		else:
			self.write("ERR")


	def writeNetwork(self):

		self.writeTitle("Network cards")
		if len(self.forensics.NetworkCards) != 0:
			for card in self.forensics.NetworkCards:
				self.write(card)
		else:
			self.write("Empty")


		self.writeTitle("IP Address")
		if len(self.forensics.IPs) != 0:
			for ip,Dict in self.forensics.IPs.iteritems():
				if ip == "Current":
					for addr in Dict:
						if len(addr) < 16:
							self.write("Currently IPv4: "+addr)
						else:
							self.write("Currently IPv6: "+addr)
				else:
					self.write("\n\t"+ip)
					for key, value in Dict.iteritems():
						self.write("\t"+(key) + ": " + value)
		else:
			self.write("Empty")


		self.writeTitle("MAC Address")
		if len(self.forensics.MACs) != 0:
			for mac in self.forensics.MACs:
				self.write(mac)
		else:
			self.write("Empty")


		if len(self.forensics.LocalNetworkMachines) != 0:
			self.writeTitle("Net view")
			for host in self.forensics.LocalNetworkMachines:
				self.write(host)


		self.writeTitle("Netstat")
		if len(self.forensics.Netstat) != 0:
			for connection in self.forensics.Netstat:
				self.write('Local: '+connection["Local"]+' | Target: '+connection["Remote"]+' | PID: '+connection["PID"]+' | App: '+connection["appName"]+' | Status: '+(connection["Status"]))
		else:
			self.write("Empty")


		self.writeTitle("ARP Table")
		if len(self.forensics.ArpTable) != 0:
			for interface, Dict in self.forensics.ArpTable.iteritems():
				self.write("\n\tInterface: "+interface)
				for known in Dict:
					self.write("IP: "+known["IP"] + " | MAC: " + known["MAC"] + " | Type: " + known["Type"])
		else:
			self.write("Empty")


		self.writeTitle("Hosts file")
		if len(self.forensics.HostsFile) != 0:
			for counter, entry in self.forensics.HostsFile.iteritems():
				if entry["TargetIP"] not in ["0.0.0.0", "127.0.0.1"]:
					self.write("Domain: "+entry["RequestedDomain"]+" | Target IP: "+entry["TargetIP"])
		else:
			self.write("Empty")



	def writeSecurity(self):

		self.writeTitle("McAfee")
		if self.forensics.McAfee["Installed"] == 0:
			self.write("McAfee not installed")
		else:
			self.write("Version: McAfee "+self.forensics.McAfee["Version"])
			self.write("DAT date: "+self.forensics.McAfee["DatDate"])
			self.write("Weekly sched: "+(str(self.forensics.McAfee["WeeklySched"])))
			self.write("Action: "+(self.forensics.McAfee["Action"]))
			self.write("Last scan: "+self.forensics.McAfee["lastScan"])
			self.write("Num quarantine files: "+str(len(self.forensics.McAfee["quarantine"])))

			if len(self.forensics.McAfee["quarantine"]) != 0:
				self.write("\n\tQuarantine files:")
				for File in self.forensics.McAfee["quarantine"]:
					self.write("\t"+File)

			if len(self.forensics.McAfee["Exclusions"]) != 0:
				self.write("\n\tExclusions:")
				for role in self.forensics.McAfee["Exclusions"]:
					if role[0] == "3":
						self.write("\tSkip file: "+role.rsplit("|",1)[1])
					elif role[0] == "4":
						self.write("\tSkip format: "+role.rsplit("|",1)[1])
					elif role[0] in ["0","1","2"]:
						self.write("\tSkip files older than "+role.rsplit("|",1)[1]+' days')
					else:
						self.write("\t"+role)

			self.write("\n\tLogs:")
			if len(self.forensics.McAfee["Logs"]) != 0:
				for log in self.forensics.McAfee["Logs"]:
					self.write("\tPath: "+log["Path"])
					self.write("\tTime: "+log["Date"])
					self.write("\tDescription: "+log["Description"])
					self.write("\tAction taken: "+(log["Action"].strip()))
					self.write("\tProcess: "+log["Process"])
					self.write("\tMD5: "+log["Hash"].strip("(MD5)"))
					self.write("")
			else:
				self.write("No interesting logs")


		self.writeTitle("Firewall")
		self.write("Status: "+self.forensics.Firewall["Status"])
		self.write("Allowed applications:")
		if len(self.forensics.Firewall["Rules"]) != 0:
			for rule in self.forensics.Firewall["Rules"]:
				self.write("\t"+rule["Name"]+" | Status: "+rule["Active"]+" | Action: "+rule["Action"])
		else:
			self.write("Empty")


		self.writeTitle("Hotfixes")
		if len(self.forensics.installedHotfixes) != 0:
			for date,hotfixList in self.forensics.installedHotfixes["Dict"].iteritems(): # the first one is the sum number
				self.write("\n\tDate: "+date)
				self.write("Packages installed: "+", ".join(hotfixList))
		else:
			self.write("Empty")



	def writeUSB(self):

		self.writeTitle("USB list")
		for x,usb in self.forensics.USB.iteritems():
			if "HID" not in usb['name'] and "Composite" not in usb['name'] and "HID" not in usb['type']:
				# Type of the USB:
				self.write(usb['name'] + " | Type: "+usb['type'] + " | Serial number: " + usb['serial'] + " | Date: " + usb['ldate'])



	def closeReportFile(self):
		self.Panorama.close()

	def openReport(self):
		startfile(PanoramaReportPage)