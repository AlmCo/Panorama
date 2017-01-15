import re

def parseFirewallRule(line):
	# Recive the value from the registry and return parsed dict of the rule
	rule = {}
	rule["Active"] = line.split("Active=")[1].split("|")[0]
	rule["App"] = line.split("App=")[1].split("|")[0]
	rule["Name"] = line.split("Name=")[1].split("|")[0]
	rule["Action"] = line.split("Action=")[1].split("|")[0]
	return rule

def parseMcAfeeDatDate(date):
	# Convert the date 2016/12/31 into 31/12/2016
	date = date.split("/")
	return date[2]+"/"+date[1]+"/"+date[0]

def parseMcAfeeLastScanDate(path):
	# Reads the end of the file OnDemandScanLog from DEFLOGDIR and parse the last date
	offset = 0
	line = ''
	with open(path+"\\"+"OnDemandScanLog.txt") as f: 
		while True: 
			offset -= 1
			f.seek(offset, 2) 
			nextline = f.next() 
			if nextline == '\n' and line.strip(): 
				return line.split("\t")[1].rsplit(":",1)[0] + " " + line.split("\t")[0]
				break
			else:
				line = nextline

def parseMcAfeeLogs(path):
	# Extract the suspicios logs
	KnownLogfilesNames = ['AccessProtectionLog.txt','OnAccessScanLog.txt','OnDemandScanLog.txt']
	Logs = []
	for logfile in KnownLogfilesNames:
		try:
			logfile = open(path+"\\"+logfile,'r').read()
			for line in logfile.split("\n"):
				parsedLine = {}
				if "trojan" in line.lower() or "deleted)" in line.lower() or "no action taken" in line.lower() or "unwanted program" in line.lower():
					if "scan timed out" not in line.lower():
						line = line.split("\t")
						parsedLine["Date"] = line[0]
						parsedLine["Time"] = line[1]
						parsedLine["Action"] = line[2]
						parsedLine["Process"] = line[4]
						parsedLine["Path"] = line[5]
						parsedLine["Description"] = line[6]
						parsedLine["Hash"] = line[7]
						Logs.append(parsedLine)
		except:
			pass
	return Logs

def parseUSB(path):
	# Build a dict of all USBs connections
	uid = 0
	USB = {}
	USBfile = open(path, 'r').read().split("<tr>")
	for usb in USBfile:
		try:
			if "<td" == usb[:3]:
				uid = uid + 1
				USB[uid]={}
				#get all values from table:
				usbparse = re.findall(r"([^>]*)[$<]", usb)
				#get the usb title:
				if "0000" in usbparse[1]:
					usbname = usbparse[2]
				else:
					usbname=usbparse[1]+" - "+usbparse[2]
				#set the usb name:
				USB[uid]['name']=usbname
				#get the usb type:
				usbtype = usbparse[3]
				USB[uid]['type']=usbtype
				#get the usb serial:
				usbserial = usbparse[9]
				USB[uid]['serial']=usbserial
				#get the first date:
				usbfdate = usbparse[10]
				USB[uid]['fdate']=usbfdate.replace(" ","|")
				#get the last date:
				usbldate = usbparse[11]
				USB[uid]['ldate']=usbldate.replace(" ","|")
		except:
			pass
	return USB

def parseUsers(output):
	return output[3:][:-1][0].split() # Remove 2 first line and 1 last line

def parseProc(proc):
	PID = ""
	Name = ""
	for line in proc.split("\n"):
		lineName = line.split(":",1)[0]
		if lineName == "PID":
			PID = line.split(":",1)[1].strip()
		if lineName == "Image Name":
			Name = line.split(":",1)[1].strip()
	
	return PID, Name

def parseConnection(line, Processes):
	connection = {}
	# Index: 0=Protocol, 1=Local, 2=Remote, 3=Status, 4=PID
	connection["Local"] = line[1].strip()
	connection["Remote"] = line[2].strip()
	connection["Status"] = line[3].strip()
	connection["Protocol"] = line[0].strip()
	connection["PID"] = line[4].strip()
	connection["appName"] = Processes[line[4].strip()]
	return connection

def parseTask(Task):
	wantedDetails = ["TaskName", "Next Run Time", "Status"]
	parsedTask = {}
	for line in Task.split("\n"):
		if line.split(":")[0] in wantedDetails:
			parsedTask[line.split(":")[0]] = line.split(":")[1].strip()

	return parsedTask

def parseHosts(hostLine):
	return hostLine.split(" ")[0], hostLine.rsplit(" ",1)[1].strip()

def parseArpTableLine(line):
	parsedLine = {}
	for value in line.split():
		if "." in value:
			parsedLine["IP"] = value
		elif "-" in value:
			parsedLine["MAC"] = value
		else:
			parsedLine["Type"] = value
	return parsedLine