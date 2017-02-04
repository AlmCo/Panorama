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

closeContent = '</div>' # for the BOX div
closeTitle = '</div>' # for the ID div


class FilesList:
	def __init__(self, contentList, PhotoList, VideoList):
		self.FilesContent = '<div id="Content" style="display:none;">'
		self.FilesPhoto = '<div id="Photo" style="display: none;">'
		self.FilesVideo = '<div id="Video" style="display: ;">'
		self.Files = open(PanoramaFilesPage, 'w')
		self.write(header)
		self.writeContent(topLogo)
		self.write("</div></div>") # Close the top
		self.write(FilesMenu)
		self.writeContentList(contentList)
		self.writePhotoList(PhotoList)
		self.writeVideoList(VideoList)
		self.closeReportFile()

	def writeContentList(self, contentList):
		self.writeContent(self.FilesContent)
		self.writeTitle("Content files")

		if len(contentList) != 0:
			self.write("<table style='word-break:break-all;'><tr><th width='75%'>File name</th><th>Created date</th></tr>")
			for cfile in contentList:
				self.writeFile(cfile)
			self.write("</table>")
		else:
			self.write("No content files")
		self.write(closeTitle)
		self.writeContent(closeContent)

	def writePhotoList(self, PhotoList):
		self.writeContent(self.FilesPhoto)
		self.writeTitle("Images")

		if len(PhotoList) != 0:
			self.write("<table style='word-break:break-all;'><tr><th width='8%'>Thumb</th><th width='70%'>Files name</th><th>Created date</th></tr>")
			for cfile in PhotoList:
				self.writeIMG(cfile)
			self.write("</table>")
		else:
			self.write("No images")

		self.write(closeTitle)
		self.writeContent(closeContent)

	def writeVideoList(self, VideoList):
		self.writeContent(self.FilesVideo)
		self.writeTitle("Video files")

		if len(VideoList) != 0:
			self.write("<table style='word-break:break-all;'><tr><th width='75%'>File name</th><th>Created date</th></tr>")
			for cfile in VideoList:
				self.writeFile(cfile)
			self.write("</table>")
		else:
			self.write("No video files")

		self.write(closeTitle)
		self.writeContent(closeContent)

	def write(self, string):
		self.Files.write(string+"<br>\n")

	def writeFile(self, string):
		name = '<font color="silver" size="3">'+string.rsplit("\\",1)[0]+'</font> '+string.rsplit("\\",1)[1]
		link = string.replace("\\","\\\\").replace("%20"," ")
		self.Files.write('<tr><td><a href="javascript:openURL(\'{}\')">\
			{}</a></td><td>{}</td></tr>\n'.format(link, name, timestamp2date(getctime(string),1)))

	def writeIMG(self, string):
		name = string.rsplit("\\",1)[1]
		link = string.replace("\\","\\\\").replace("%20"," ")
		self.Files.write('<tr><td><img src="{}" width="40" height="25"></td><td><a href="javascript:openURL(\'{}\')">\
			{}</a></td><td>{}</td></tr>\n'.format(link, link, name, timestamp2date(getctime(string),1)))

	def writeContent(self, string):
		self.Files.write(string+"\n")

	def writeTitle(self, title):
		self.Files.write('<div class="box">\
			<div class="title">'+title+'</div><hr>')

	def closeReportFile(self):
		self.Files.close()

	def openReport(self):
		startfile(PanoramaFilesPage)


class HTMLReport:
	def __init__(self, forensics):
		self.OSContent = '<div id="OS" style="display: ;">'
		self.NetworkContent = '<div id="Network" style="display: none;">'
		self.SecurityContent = '<div id="Security" style="display: none;">'
		self.USBContent = '<div id="USB" style="display: none;">'
		self.forensics = forensics
		self.Panorama = open(PanoramaReportPage, 'w')
		self.write(header)
		self.writeContent(topLogo)
		self.writeOSDetails()
		self.write(ReportMenu)
		self.writeOS()
		self.writeNetwork()
		self.writeSecurity()
		self.writeUSB()
		self.closeReportFile()

	def write(self, string, line=1):
		self.Panorama.write(string+"<br>\n")

	def writeContent(self, string):
		self.Panorama.write(string+"\n")

	def writeTitle(self, title):
		self.Panorama.write('<div class="box">\
			<div class="title">'+title+'</div><hr>')
	
	def writeOSDetails(self):
		self.write("Hostname: "+self.forensics.hostname)
		self.write("Serial number: "+self.forensics.serialnumber)
		self.write("OS: "+self.forensics.OS["ProductName"]+" "+self.forensics.OS["SP"]+" "+self.forensics.OS["Bit"])
		self.write("OS Install date: "+self.forensics.OS["InstallDate"])
		self.write("Num of hotfixes: "+str(self.forensics.installedHotfixes["Sum"]))
		self.write("Firewall status: "+(self.forensics.Firewall["Status"]))
		self.write('</div><div style="clear: both;"></div></div>') # this is close the top
	
	def writeOS(self):
		self.writeContent(self.OSContent)
		self.writeTitle("Users")
		for user in self.forensics.Users:
			if user not in ["Guest", "DefaultAccount"]:
				self.write("<b>"+user+"</b>")
				for value in self.forensics.Users[user]:
					self.write((value)+": "+(str(self.forensics.Users[user][value])))
				self.write(" ")
		self.write(closeTitle)


		self.writeTitle("Commands on startup")
		if len(self.forensics.CommandsOnStartup) != 0:
			table = ("<table><tr><th width='90%'>Command</th><th>Process active now</th></tr>")
			for command,active in self.forensics.CommandsOnStartup.iteritems():
				try:
					table += ("<tr><td>%s</td><td>%s</td></tr>\n" % (command,(str(active))))
				except:
					print "ERROR: 6349"
					print command
			self.write(table+"</table>")
		else:
			self.write("Empty")
		self.write(closeTitle)


		self.writeTitle("Task scheduler")
		if len(self.forensics.Tasks) != 0:
			table = ("<table><tr><th>Name</th><th>Execute date</th><th>Status</th></tr>")
			for task in self.forensics.Tasks:
				table+= "<tr><td>"+task["TaskName"]+"</td><td>"+task["Next Run Time"]+"</td><td>"+task["Status"]+"</td></tr>"
			self.write(table+"</table>")
		else:
			self.write("Empty")
		self.write(closeTitle)


		self.writeTitle("Installed softwares")
		rowCount = 0
		if len(self.forensics.SoftwareList) != 0:
			blacklist = ['utorrent', 'teraterm', 'logmein', 'flashfxp', 'bittorrent', 'bitorrent', 'tor','teamviewer','skype','icq','emule','kazaa','dropbox','apple','itunes','wireless','havij','popcorn', 'torbrowser', 'logmett', 'join.me', 'popcorn time']
			table = "<table>"
			for software in self.forensics.SoftwareList:
				if rowCount == 3:
					table += ("</tr>\n<tr>")
					rowCount = 0
				try:
					if software.lower() in blacklist:
						table += ('<td style="word-break:break-all; width: 25%; background: #ff5050;">{}</td>\n'.format(software.encode('utf-8')))
					else:
						table += ('<td style="word-break:break-all; width: 25%;">{}</td>\n'.format(software.encode('utf-8')))
					rowCount += 1
				except:
					pass
			self.write(table+"</table>")
		else:
			self.write('Empty')
		self.write(closeTitle)


		self.writeTitle("Recently used files")
		rowCount = 0
		if len(self.forensics.Recent) != 0:
			table = "<table>"
			for each in self.forensics.Recent:
				if rowCount == 3:
					table += ("</tr>\n<tr>")
					rowCount = 0
				table += ('<td style="word-break:break-all; width: 25%;"><a href="javascript:openURL(\'{}\')">{}</a></td>\n'.format(each.replace("\\","\\\\"), each.rsplit("\\",1)[1].replace(".lnk","")))
				rowCount += 1

			self.write(table+"</table>")
		else:
			self.write('0 Recent files')
		self.write(closeTitle)


		self.writeTitle("Active processes")
		if len(self.forensics.Processes) != 0:
			table = ("<table><tr><th>Name</th><th>ID</th><th>Communicating</th></tr>")
			for pid,name in self.forensics.Processes.iteritems():
				if name.strip() not in ["System", "System Idle Process"]:
					if str(self.forensics.Netstat).find(str(name+"', 'PID': '"+str(pid))) == -1:
						table += ("<tr><td>"+name+"</td><td>"+str(pid)+"</td><td>No</td></tr>\n")
					else:
						table += ("<tr><td>"+name+"</td><td>"+str(pid)+"</td><td><b>Yes</b></td></tr>\n")
			self.write(table+"</table>")
		else:
			self.write("ERR")
		self.write(closeTitle)

		self.writeContent(closeContent)

	def writeNetwork(self):
		self.writeContent(self.NetworkContent)

		self.writeTitle("Network cards")
		if len(self.forensics.NetworkCards) != 0:
			wirelessWords = ["wireless", "802"]
			for card in self.forensics.NetworkCards:
				writed = 0
				for word in wirelessWords:
					if card.lower().find(word) != -1 and writed == 0:
						self.write('<font color="red">'+card+"</font>")
						writed = 1
				if writed == 0:
					self.write(card)
		else:
			self.write("Empty")
		self.write(closeTitle)


		self.writeTitle("IP Address")
		if len(self.forensics.IPs) != 0:
			for ip,Dict in self.forensics.IPs.iteritems():
				if ip == "Current":
					ips = ""
					for addr in Dict:
						if len(addr) < 16:
							ips += "IPv4 - "+addr+"<br>"
						else:
							ips += "IPv6 - "+addr+"<br>"
					self.write("<b>Currently IPs:</b><br>"+ips)
				else:
					singleIP = "<br><b>"+ip+"</b>"
					for key, value in Dict.iteritems():
						singleIP += "<br><b>"+(key) + ":</b> " + value
					self.write(singleIP)
		else:
			self.write("Empty")
		self.write(closeTitle)


		self.writeTitle("MAC Address")
		if len(self.forensics.MACs) != 0:
			for mac in self.forensics.MACs:
				self.write(mac)
		else:
			self.write("Empty")
		self.write(closeTitle)


		if len(self.forensics.LocalNetworkMachines) != 0:
			self.writeTitle("Net view")
			for host in self.forensics.LocalNetworkMachines:
				self.write(host)
			self.write(closeTitle)


		self.writeTitle("Netstat")
		if len(self.forensics.Netstat) != 0:
			table = "<table><tr><th>Local</th><th>Target</th><th>ID</th><th>Process</th><th>Status</th></tr>\n"
			for connection in self.forensics.Netstat:
				table += '<tr><td style="word-break:break-all;">'+connection["Local"]+'</td><td style="word-break:break-all;">'+connection["Remote"]+'</td><td>'+connection["PID"]+'</td><td style="word-break:break-all;">'+connection["appName"]+'</td><td>'+(connection["Status"])+'</td></tr>\n'
			self.write(table+"</table>")
		else:
			self.write("Empty")
		self.write(closeTitle)


		self.writeTitle("ARP Table")
		if len(self.forensics.ArpTable) != 0:
			for interface, Dict in self.forensics.ArpTable.iteritems():
				table = "<table><tr><th>"+interface+"</th></tr><tr><th>IP</th><th>MAC</th><th>Type</th></tr>\n"
				for known in Dict:
					table += "<tr><td>"+known["IP"] + "</td><td>" + known["MAC"] + "</td><td>" + known["Type"] + "</td></tr>\n"
				self.write(table+"</table>")
		else:
			self.write("Empty")
		self.write(closeTitle)


		self.writeTitle("Hosts file")
		if len(self.forensics.HostsFile) != 0:
			table = "<table><tr><th>Domain</th><th>Target IP</th></tr>"
			for counter, entry in self.forensics.HostsFile.iteritems():
				if entry["TargetIP"] not in ["0.0.0.0", "127.0.0.1"]:
					table += "<tr><td>"+entry["RequestedDomain"]+"</td><td>"+entry["TargetIP"]+"</td></tr>"
			self.write(table+"</table>")
		else:
			self.write("Empty")
		self.write(closeTitle)


		self.writeContent(closeContent)

	def writeSecurity(self):
		self.writeContent(self.SecurityContent)

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
				self.write("<br><b>Quarantine files:</b>")
				for File in self.forensics.McAfee["quarantine"]:
					self.write(File)

			if len(self.forensics.McAfee["Exclusions"]) != 0:
				self.write("<br><b>Exclusions:</b>")
				for role in self.forensics.McAfee["Exclusions"]:
					if role[0] == "3":
						self.write("Skip file: "+role.rsplit("|",1)[1])
					elif role[0] == "4":
						self.write("Skip format: "+role.rsplit("|",1)[1])
					elif role[0] in ["0","1","2"]:
						self.write("Skip files older than "+role.rsplit("|",1)[1]+' days')
					else:
						self.write(role)

			self.write("<br><b>Logs:</b>")
			if len(self.forensics.McAfee["Logs"]) != 0:
				for log in self.forensics.McAfee["Logs"]:
					self.write("<b>Path: </b>"+log["Path"])
					self.write("<b>Time: </b>"+log["Date"])
					self.write("<b>Description: </b>"+log["Description"])
					self.write("<b>Action taken: </b>"+(log["Action"].strip()))
					self.write("<b>Process: </b>"+log["Process"])
					self.write("<b>MD5: </b>"+log["Hash"].strip("(MD5)"))
					self.write("")
			else:
				self.write("No interesting logs")
		self.write(closeTitle)


		self.writeTitle("Firewall")
		self.write("<b>Status: </b>"+self.forensics.Firewall["Status"]+"<br>")
		self.write("<b>Allowed applications:</b>")
		if len(self.forensics.Firewall["Rules"]) != 0:
			table = "<table><tr><th>Name</th><th>Active</th><th>Action</th></tr>"
			for rule in self.forensics.Firewall["Rules"]:
				table += "<tr><td>"+rule["Name"]+"</td><td>"+rule["Active"]+"</td><td>"+rule["Action"]+"</td></tr>"
			self.write(table+"</table>")
		else:
			self.write("Empty")
		self.write(closeTitle)


		self.writeTitle("Hotfixes")
		if len(self.forensics.installedHotfixes) != 0:
			for date,hotfixList in self.forensics.installedHotfixes["Dict"].iteritems(): # the first one is the sum number
				self.write("<br><b>Date: </b>"+date)
				self.write("<b>Packages installed: </b>"+", ".join(hotfixList))
		else:
			self.write("Empty")
		self.write(closeTitle)


		self.writeContent(closeContent)

	def writeUSB(self):
		self.writeContent(self.USBContent)

		self.writeTitle("USB list")
		knownDict = {'belkin': 'smart', 'meizu': 'smart', 'galaxy': 'smart', 'lg': 'smart', 'tablet': 'smart', 'flash': 'storage', 'black': 'smart', 'dlink': 'network', 'smart': 'smart', 'sm-g920': 'smart', 'g4': 'smart', 'g3': 'smart', 'gadget': 'smart', 'nokia': 'smart', 'watch': 'smart', 'dell': 'smart', 'toshiba': 'storage', 'band': 'network', 'sony': 'smart', 'lumia': 'smart', 'motorola': 'smart', 'xbox': 'smart', 'blackberry': 'smart', 'google': 'smart', 'htc': 'smart', 'portable': 'storage', '256gb': 'storage', 'bluetooth': 'network', 'hitachi': 'storage', 'gt-i9300': 'smart', 'huawei': 'smart', 'cdram': 'disk', 'net': 'network', 'wd': 'storage', '128gb': 'storage', 'dualband': 'network', 'ipod': 'smart', '4gb': 'storage', 'web': 'smart', 'sandisk': 'storage', 'tplink': 'network', '8gb': 'storage', 'apple': 'smart', 'corsair': 'storage', 'linux': 'smart', 'gt-i9200': 'smart', 'jetflash': 'storage', '802.11': 'network', 'camera': 'camera', 'iphone': 'smart', 'safenet': 'license', 'gt-i9100t': 'smart', 'webcam': 'camera', 'floppy': 'storage', '64gb': 'storage', 'wireless': 'network', 'phone': 'smart', '32gb': 'storage', 'datatravel': 'storage', 'ipad': 'smart', 'patriot': 'storage', 'sm-g900i': 'smart', 'sm-g900f': 'smart', 'budget': 'smart', 'windows': 'smart', '802.11ac': 'network', 'cam': 'camera', '16gb': 'storage', '802.11a': 'network', 'transcend': 'storage', 'ac': 'network', '802.11b': 'network', '802.11g': 'network', 'nexus': 'smart', 'kingston': 'storage', 'canon': 'camera', '802.11n': 'network', 'sm-g920i': 'smart', 'tab': 'smart', 'acer': 'smart', 'sm-g920f': 'smart', 'cddvd': 'disk', 'gt-i9100': 'smart', 'dvdram': 'disk', 'generic': 'storage', 'storage': 'storage', 'note': 'smart', 'android': 'smart', 'lan': 'network', 'nic': 'network', 'powershot': 'camera', 'tp-link': 'network', 'ethernet': 'network', 'nikon': 'camera', 'linksys': 'network', 'samsung': 'smart', 'mobile': 'smart', 'sm-g900': 'smart', 'd-link': 'network', 'link': 'network', 'oneplus': 'smart'}
		for x,usb in self.forensics.USB.iteritems():
			if "HID" not in usb['name'] and "Composite" not in usb['name'] and "HID" not in usb['type']:
				writeUSB = "<br><b>"+usb['name']+"</b>"
				for word in usb['name'].split():
					# Try to say what is the USB
					if word.lower() in knownDict:
						writeUSB += "<br><b>Description: </b>"+knownDict[word.lower()]+" device"
						break

				# Type of the USB:
				writeUSB += "<br><b>Type: </b>"+usb['type']
				writeUSB += "<br><b>Serial number: </b>"+usb['serial']
				writeUSB += "<br><b>Date: </b>"+usb['ldate']

				self.write(writeUSB)
		self.write(closeTitle)


		self.writeTitle("USBDeview")
		self.write('<a href="'+PanoramaDir+'\usbdeview.html" target="_blank"><b>> Open the original table <</b></a>')
		self.write(closeTitle)

		self.writeContent(closeContent)

	def closeReportFile(self):
		self.Panorama.close()

	def openReport(self):
		startfile(PanoramaReportPage)



topLogo = '<div style="width: 80%; font-size: 20px; color: #fff; margin-right: auto; margin-left: auto;">\
			<div style="float: left;"><img src="'+WebLogo.strip(" ")+'" width="350px"></div>\
			<div style="float: right;">'

ReportMenu = """
		<div class="menu">
		<a href="javascript:show(\'OS\')"><div class="menuButton">System</div></a>
		<a href="javascript:show(\'Network\')"><div class="menuButton">Network</div></a>
		<a href="javascript:show(\'USB\')"><div class="menuButton">USB</div></a>
		<a href="javascript:show(\'Security\')"><div class="menuButton">Security</div></a>
		</div>"""

FilesMenu = """
		<div class="menu">
		<a href="javascript:show(\'Video\')"><div class="menuButton">Video</div></a>
		<a href="javascript:show(\'Photo\')"><div class="menuButton">Images</div></a>
		<a href="javascript:show(\'Content\')"><div class="menuButton">Content</div></a>
		</div>"""

header = """<html>
			<!-- Writed by Almog Cohen - almogcn@gmail.com -->
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
			<html><head>
			  <title>Panorama - Fast incident overview</title>
			<style>
			body {
				background-color: #072144;
				margin-left: auto;
				margin-right: auto;
				font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif;m,
			}

			.menu {
				width: 100%;
				font-size: 36px;
				background-color: #d6d3d6;
				text-align: center;
				padding-top: 5px;
				padding-bottom: 7px;
			}

			.menuButton{
				display: inline-block;
				*display:inline;
				zoom:1;
				text-align: center;
				margin-left: 27px;
				margin-right: 27px;
			}

			.title {
				font-size: 27px;
				text-align: left;
				padding-left: 12px;
				padding-top: 5px;
				font-weight: bold;
			}

			hr {
				max-width: 98%;
				border: 0;
				height: 1px;
				background-color: #092730;
			}

			.box {
				font-size: 19px;
				background-color: #efefef;
				width: 85%;
				margin-top: 10px;
				margin-bottom: 15px;
				margin-right: auto;
				margin-left: auto;
				padding: 12px;
				line-height: 1.3;
			}

			table{
				border-collapse: collapse;
				border-spacing: 0;
				font-size: 18px;
				width: 98%;
			}

			tr:nth-child(even){background: #f2f2f2;}

			tr:hover {
				background: #DADADA;
				color: #000;
			}

			td:hover {
				background: #cfcfcf;
			}

			td {
				padding: 4px;
				border: 1px solid #dedede;
			}

			th{background-color: #e6e6e6;}


			a {text-decoration: none; color: #00317B;}
			a:hover{text-decoration: underline; color:#8b8b8b;}
			.menu a{color:#8b8b8b;}
			.menu a:hover{color:#071e29;}
			.menu a:active{color:#071e29;}
			</style></head>
			<body>
			<script type="text/javascript">
				var all = ["OS", "Video", "Network", "USB", "Photo", "Security", "Content"]
				function show(element){
					document.getElementById(element).style.display = "";
					for (var i = 0; i < all.length; i++){
						if (all[i] != element){
							try{
								hideThis(all[i]);
							}
							catch(err){}
						}
					};
				}

				function hideThis(element){
					document.getElementById(element).style.display = "none";
				}

				function openURL(url) {
					var myWindow = window.open(url, "", "width=500,height=500");
				}
			</script>
			"""
