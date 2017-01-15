from os import popen

from lib.Registry import *

def cmd(command):
	# Using for single command from cmd
	return popen(command).read().strip().split("\n")

def getServicePack():
	# Parse the service pack of the system
	spDict = {"0":"SP0", "256":"SP1", "512":"SP2", "768":"SP3", "1024":"SP4"}
	try:
		sp = readName(r"SYSTEM\CurrentControlSet\Control\Windows",'CSDVersion')
		return spDict[str(sp)]
	except:
		return "SP0"

def getOSArch():
	# Parse how many Bit this processor
	if "86" in readName(r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",'PROCESSOR_ARCHITECTURE'):
		return "32Bit"
	else:
		return "64Bit"

def getMcAfeeSchedStatus(Bit):
	# Checks if full scan schedule is set at least for every 7 days
	if "64" in Bit: # 64Bit host
		if int(readName(r"Software\Wow6432Node\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}",'bSchedEnabled')) == 1:
			if int(readName(r"Software\Wow6432Node\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}",'Weekly_maskDaysOfWeek')) != 0 and int(readName(r"Software\Wow6432Node\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}",'Weekly_nRepeatWeeks')) == 1: return 1
			if int(readName(r"Software\Wow6432Node\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}",'Daily_nRepeatDays')) < 8: return 1
		return 0
	else: # x32Bit host
		if int(readName(r"Software\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}",'bSchedEnabled')) == 1:
			if int(readName(r"Software\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}",'Weekly_maskDaysOfWeek')) != 0 and int(readName(r"Software\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}",'Weekly_nRepeatWeeks')) == 1: return 1
			if int(readName(r"Software\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}",'Daily_nRepeatDays')) < 8: return 1
		return 0

def getMcAfeeAction(Bit):
	if "64" in Bit: # 64Bit host
		if readName(r"SOFTWARE\Wow6432Node\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}",'uAction_Program') in ["4","5"]: return "Delete"
		if readName(r"SOFTWARE\Wow6432Node\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}",'uAction') in ["4","5"]: return "Delete"
		return "Scan"
	else: # x32Bit host
		if readName(r"SOFTWARE\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}",'uAction_Program') in ["4","5"]: return "Delete"
		if readName(r"SOFTWARE\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}",'uAction') in ["4","5"]: return "Delete"
		return "Scan"

def getMcAfeeExclusions(Bit):
	if "64" in Bit: # 64Bit host
		query = readValues(r"SOFTWARE\Wow6432Node\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}")
	else: # x32Bit host
		query = readValues(r"SOFTWARE\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}")

	Exclusions = []
	for name, value in query.iteritems():
		if name.lower()[:13] == "excludeditem_":
			Exclusions.append(value)
	return Exclusions

def getCurrentIPs():
	LiveIPs = []
	current = cmd('ipconfig | find "IP"')[1:] # the 1: is to avoid the first printed junk line
	for ip in current:
		try:
			LiveIPs.append(ip.split(":",1)[1].strip())
		except Exception as e:
			print e
	return LiveIPs

def getActiveProcesses():
	return popen("tasklist /FO LIST").read().strip().split("\n\n")

def getTaskschList():
	return popen("schtasks /Query /FO LIST").read().strip().split("\n\n")

def getHostsFileContent():
	return open("c:\windows\system32\drivers\etc\hosts",'r').readlines()

def getArpTable():
	return popen("arp -a").read().strip().split("\n\n")