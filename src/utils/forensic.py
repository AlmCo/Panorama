# -*- coding: utf-8 -*-

import sys

from utils.HTML import timestamp2date
from lib.Registry import *
from common.paths import *
from utils.parsers import *
from utils.getters import *

# To do:
# Networks the computer was joined
# Mapped shares

reload(sys)
sys.setdefaultencoding("utf-8")

class Forensic:
	def __init__(self):
		self.hostname = readName(r"SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName",'ComputerName')
		self.OS = {}
		self.serialnumber = ""
		self.Firewall = {}
		self.installedHotfixes = {} # Install date : [KBs]
		self.McAfee = {}
		self.USB = {}
		self.NetworkCards = {} # Card name : Type
		self.Users = {} # Dict of Dicts = Username {Admin, Password last set, Last logon, Password required, Account active, Password expires}
		self.SoftwareList = set() # Uniqe list of Installed softwares
		self.IPs = {} # Dict of IP : Date, DHCPServer
		self.MACs = set() # Uniqe list of MAC address
		self.Processes = {} # Dict of PID : Name
		self.CommandsOnStartup = {} # Dict of name of the command : if its currently running
		self.Netstat = [] # List of Dict's of all connections - Dict includes: ip addresses, protocol, app name, pid and status
		self.Tasks = [] # List of Dict's of all tasks - Dict includes: name, next run date and status
		self.HostsFile = {} # Dict's of all entries - Dict includes: counted number, requested domain and target ip
		self.LocalNetworkMachines = [] # List of hostnames on the network
		self.ArpTable = {} # Dict of ARP table by interface, every interface have his own arp table
		self.Recent = [] # List of recent files

	def fOS(self):
		# Fills the OS dict by the description
		try:
			self.OS["ProductName"] = readName(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",'ProductName')
		except:
			self.OS["ProductName"] = "0"

		try:
			self.OS["SP"] = getServicePack()
		except:
			self.OS["ProductName"] = "0"

		try:
			self.OS["Bit"] = getOSArch()
		except:
			self.OS["Bit"] = "0"

		try:
			self.OS["InstallDate"] = timestamp2date(readName(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",'InstallDate'), 1)
		except:
			self.OS["InstallDate"] = "0"

	def fSerialNumber(self):
		# Extract the embeded serial number by WMIC
		try:
			wmicSerial = cmd("wmic bios get serialnumber")[1]
			if wmicSerial not in ["To be filled by O.E.M.", "Default string"]:
				self.serialnumber = wmicSerial
			else:
				self.serialnumber = "000000"
		except:
			self.serialnumber = "000000"

	def fHotfixs(self):
		# Parse all of the installed hotfixes into a dict:
		# TO DO: Parse it out from the registry to avoid the CMD command.
		# Example of return: {'Sum': 4, 'Dict': {'1/14/2016': ['KB2425227', 'KB2533552', 'KB2534366', 'KB971412']}}
		self.installedHotfixes = {"Sum":0, "Dict":{}} 
		try:
			kblist = cmd("wmic qfe get hotfixid,installedon")
			for i in kblist:
				try:
					if i[:2] == "KB":
						self.installedHotfixes["Sum"] += 1
						kbNum,installDate = i.split()
						if installDate in self.installedHotfixes["Dict"]:
							self.installedHotfixes["Dict"][installDate].append(kbNum)
						else:
							self.installedHotfixes["Dict"][installDate] = []
							self.installedHotfixes["Dict"][installDate].append(kbNum)
				except:
					pass
		except Exception as e:
			print e
			self.installedHotfixes["Sum"] = -1 # Return -1 to report the error

	def fFirewall(self):
		# Checks firewall status
		try:
			StandardProfile = readName(r"SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile",'EnableFirewall')
		except:
			StandardProfile = "0" # Never was enabled so the reg key wasnt created
		
		if StandardProfile.find("1") != -1:
			self.Firewall["Status"] = "ON"
		else:
			self.Firewall["Status"] = "OFF"

		# Load the firewall rules:
		self.Firewall["Rules"] = []
		try:
			rulesDict = readValues(r"SYSTEM\CurrentControlSet\services\SharedAccess\Parameters\FirewallPolicy\FirewallRules")
			for name, value in rulesDict.iteritems():
				try:
					rule = parseFirewallRule(value)
					if rule["Active"] == "TRUE" and rule["Action"] == "Allow" and "FirewallAPI.dll" not in rule["Name"]:
						self.Firewall["Rules"].append(rule)
				except:
					pass
		except:
			pass # No rules

	def fMcAfee(self):
		try:
			self.McAfee["Installed"] = 1
			if "64" in self.OS["Bit"]:
				self.McAfee["Version"] = readName(r"Software\Wow6432Node\McAfee\DesktopProtection",'szProductVer')
				self.McAfee["DatDate"] = parseMcAfeeDatDate(readName(r"Software\Wow6432Node\McAfee\AVEngine",'AVDatDate'))
			else:
				self.McAfee["Version"] = readName(r"Software\McAfee\DesktopProtection",'szProductVer')
				self.McAfee["DatDate"] = parseMcAfeeDatDate(readName(r"Software\McAfee\AVEngine",'AVDatDate'))

			self.McAfee["LogDir"] = readName(r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",'DEFLOGDIR')
			self.McAfee["WeeklySched"] = getMcAfeeSchedStatus(self.OS["Bit"]) # Registry path is diffrent from 64Bit to 32Bit
			self.McAfee["Action"] = getMcAfeeAction(self.OS["Bit"]) # Registry path is diffrent from 64Bit to 32Bit
			self.McAfee["Exclusions"] = getMcAfeeExclusions(self.OS["Bit"]) # Registry path is diffrent from 64Bit to 32Bit
			self.McAfee["lastScan"] = parseMcAfeeLastScanDate(self.McAfee["LogDir"])
			self.McAfee["Logs"] = parseMcAfeeLogs(self.McAfee["LogDir"])
			self.McAfee["quarantine"] = listdir("C:\quarantine")
		except:
			self.McAfee["Installed"] = 0


	def fUSB(self):
		cmd(PanoramaDir+"\USBDeview.exe /shtml "+PanoramaDir+"\usbdeview.html")
		try:
			self.USB = parseUSB(PanoramaDir+"\usbdeview.html")
		except:
			pass

	def fNetworkCards(self):
		# Check on USB plugs:
		networds = ['wireless','lan','bluetooth','ethernet','802.11','nic','802.11n','802.11a','802.11ac','802.11g','802.11b','net','tplink','tp-link','linksys','dlink','d-link','link','band','dualband','dsl','netstick']
		for uid,usb in self.USB.iteritems():
			try:
				usbname = usb["name"]+" - "+usb["type"]
				if any(word in usbname.lower() for word in networds):
					self.NetworkCards[usbname] = "Wireless"
			except:
				pass

		# Check on registry
		try:
			networkCards = readKeys(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkCards")
			for card in networkCards:
				try:
					cardName = readName(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkCards\%s" % card, "Description")
					self.NetworkCards[cardName] = "Network"
				except:
					pass
		except:
			pass

	def fUsers(self):
		wantedDetails = ["Password last set", "Last logon", "Password required", "Account active", "Password expires"]
		try:
			usersList = parseUsers(cmd("net user"))
			for user in usersList:
				self.Users[user] = {}
				userDetails = cmd("net user "+user)

				# Check if this user in administrators group
				if str(userDetails).find("Administrators") != -1:
					self.Users[user]["admin"] = "Yes"
				else:
					self.Users[user]["admin"] = "No"

				for line in userDetails:
					for lineInfo in line.split("\t"):
						try:
							valueName = lineInfo.split("  ")[0]
							if valueName in wantedDetails:
								self.Users[user][valueName] = lineInfo.rsplit("  ",1)[1]
						except:
							pass
		except:
			pass

	def fSoftwareList(self):
		try:
			# Registry Uninstall path:		
			for software in readKeys(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"):
				if "{" != software[0]:
					try:
						software = readName(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",'DisplayName')
					except:
						pass # No display name - take the key name
					self.SoftwareList.add(software)
		except:
			pass

		# Installed DIRs and merage the set lists:
		try:
			self.SoftwareList |= set(listdir("C:\Program Files"))
		except:
			pass


		if "64" in self.OS["Bit"]:
			try:
				self.SoftwareList |= set(listdir("C:\Program Files (x86)"))
			except:
				pass

		try:
			self.SoftwareList |= set(listdir(appdata))
		except:
			pass

		try:
			self.SoftwareList |= set(listdir(appdata.replace("Roaming","Local")))
		except:
			pass

		try:
			self.SoftwareList |= set(listdir(appdata.replace("Roaming","LocalLow")))
		except:
			pass

	def fIPs(self):
		try:
			for ip in readKeys(r"SYSTEM\CurrentControlSet\services\Tcpip\Parameters\Interfaces"):
				try:
					try:
						ipAddress = readName(r"SYSTEM\CurrentControlSet\services\Tcpip\Parameters\Interfaces\%s" % ip, 'DhcpIPAddress')
					except:
						ipAddress = readName(r"SYSTEM\CurrentControlSet\services\Tcpip\Parameters\Interfaces\%s" % ip, 'IPAddress')

					ipAddress = ipAddress.strip(" []'u")
					if ipAddress != "0.0.0.0":
						self.IPs[ipAddress] = {}
						self.IPs[ipAddress]["Time"] = timestamp2date(readName(r"SYSTEM\CurrentControlSet\services\Tcpip\Parameters\Interfaces\%s" % ip, 'LeaseObtainedTime'), 1)
						self.IPs[ipAddress]["DhcpServer"] = readName(r"SYSTEM\CurrentControlSet\services\Tcpip\Parameters\Interfaces\%s" % ip, 'DhcpServer')

				except:
					pass # Not really used IP address
		except:
			pass

		try:
			self.IPs["Current"] = getCurrentIPs()
		except:
			pass

	def fMACs(self):
		try:
			for MAC in cmd('ipconfig /all | find "Physical Address"'):
				try:
					self.MACs.add(MAC.split(":",1)[1])
				except:
					pass
		except:
			pass

	def fProcesses(self):
		whitelist = ["audiodg.exe","conhost.exe","csrss.exe","lsass.exe","lsm.exe","MSCamS64.exe","McTray.exe","alg.exe","naPrdMgr.exe","OSPPSVC.EXE","PresentationFontCache.exe","SearchIndexer.exe","services.exe","smss.exe","spoolsv.exe","svchost.exe","System","SystemIdleProcess","UNS.exe","wininit.exe","WmiApSrv.exe","WmiPrvSE.exe","wmpnetwk.exe","WUDFHost.exe","chrome.exe","atiesrxx.exe","stacsv64.exe","tasklist.exe","conhost.exe","SmartMenu.exe","explorer.exe","explore.exe","taskhost.exe","cmd.exe","LogonUI.exe","jusched.exe","dllhost.exe","taskeng.exe","TrustedInstaller.exe","shstat.exe","winlogon.exe","ctfmon.exe","mcshield.exe","WLIDSVC.EXE","notepad.exe","VsTskMgr.exe","mfeann.exe","RtkNGUI64.exe","mfevtps.exe"]
		try:
			for proc in getActiveProcesses():
				try:
					pid, pname = parseProc(proc)
					self.Processes[pid] = pname
				except:
					pass
		except:
			pass

	def fCommandsOnStartup(self):
		# Registry of x86 Bit:
		try:
			run = readValues(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
			for name,command in run.iteritems():
				self.CommandsOnStartup[command] = 0
		except:
			pass

		try:
			runonce = readValues(r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce")
			for name,command in runonce.iteritems():
				self.CommandsOnStartup[command] = 0
		except:
			pass

		# Registry of x64 Bit:
		if "64" in self.OS["Bit"]:
			try:
				run = readValues(r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run")
				for name,command in run.iteritems():
					self.CommandsOnStartup[command] = 0
			except:
				pass

			try:
				runonce = readValues(r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce")
				for name,command in runonce.iteritems():
					self.CommandsOnStartup[command] = 0
			except:
				pass
		
		try:
			# Startup folder of user AppData:
			startupDirPath = appdata+"\Microsoft\Windows\Start Menu\Programs\Startup"
			if isdir(startupDirPath):
				startupDir = listdir(startupDirPath)
				for sFile in startupDir:
					try:
						if sFile != "desktop.ini":
							self.CommandsOnStartup[sFile] = 0
					except:
						pass
		except:
			pass

		try:
			# Check which of the startup commands are running right now:
			for command in self.CommandsOnStartup:
				try:
					if (str(self.Processes).lower()).find(command.rsplit(".",-1)[0].rsplit("\\",1)[1].lower()) != -1:
						self.CommandsOnStartup[command] = 1
				except Exception as e:
					print e
		except:
			pass

	def fNetStat(self):
		try:
			netstatTable = cmd("netstat -no")[3:]
			for line in netstatTable:
				try:
					connection = filter(None,line.split("  "))
					self.Netstat.append(parseConnection(connection, self.Processes))
				except:
					pass
		except:
			pass

	def fTasks(self):
		try:
			for task in getTaskschList():
				try:
					if "\Microsoft\Windows" not in task: # Hide all defaults
						parsedTask = parseTask(task)
						if parsedTask and parsedTask not in self.Tasks:
							self.Tasks.append(parsedTask)
				except:
					pass
		except:
			pass

	def fHosts(self):
		try:
			HostsFileContent = getHostsFileContent()
			count = 0
			for line in HostsFileContent:
				try:
					if line[0] != "#":
						try:
							ip, domain = parseHosts(line)
							self.HostsFile[count] = {}
							self.HostsFile[count]["TargetIP"] = ip
							self.HostsFile[count]["RequestedDomain"] = domain
							count += 1
						except:
							pass
				except:
					pass
		except:
			pass

	def fLocalNetworkMachines(self):
		try:
			for hostname in cmd("net view")[3:-1]:
				try:
					self.LocalNetworkMachines.append(hostname.strip().replace("\\\\",""))
				except:
					pass
		except:
			pass

	def fArpTable(self):
		try:
			arptable = getArpTable()
			for interface in arptable:
				try:
					localIP = interface.split("Interface:")[1].split("--")[0].strip()
					self.ArpTable[localIP] = []
					for line in interface.split("Type")[1].split("\n"):
						if len(line) > 1: self.ArpTable[localIP].append(parseArpTableLine(line))
				except:
					pass
		except:
			pass

	def fRecent(self):
		try:
			RecentDirPath = appdata+"\Microsoft\Windows\Recent"
			if isdir(RecentDirPath):
				listRecentDirPath = listdir(RecentDirPath)
				for rfile in listRecentDirPath:
					try:
						self.Recent.append(appdata+"\Microsoft\Windows\Recent\%s" % rfile.decode('iso8859_8').replace("?","\\"))
					except:
						pass
		except:
			pass



forensic = Forensic()