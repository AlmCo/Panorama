# -*- coding: utf-8 -*-

################################################################################
################################################################################
######
###### Panorama v1.0 - Fast incident overview
###### Support and tested: Windows 2000 and up
######
###### Description:
###### Generate quick report include firewall policy, network status, startup commands, task scheduler, prefetch files,
###### history of usb connections, McAfee logs, sound and record, running proccess and general stuff.
######
###### Writed by Almog Cohen - almogcn@gmail.com
###### Github page: https://github.com/AlmCo/Panorama
######
################################################################################
################################################################################

import os, _winreg, re, datetime, tkMessageBox, webbrowser, ctypes
from Tkinter import *
import sys, pyaudio, wave

reload(sys)
sys.setdefaultencoding("utf-8")

print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
cmdlogo = """
  _____                                            
 |  __ \                                           
 | |__) |_ _ _ __   ___  _ __ __ _ _ __ ___   __ _ 
 |  ___/ _` | '_ \ / _ \| '__/ _` | '_ ` _ \ / _` |
 | |  | (_| | | | | (_) | | | (_| | | | | | | (_|.|
 |_|   \__,_|_| |_|\___/|_|  \__,_|_| |_| |_|\__,_|

              Fast incident overview                   v1.0                    
"""
print cmdlogo
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
print "0%   -    25%      -       50%      -      75%     -    100%"
print "------------------------------------------------------------"

tempfolder = str(os.popen("echo %temp%").read().split("\n")[0])
if os.path.isdir(tempfolder+"\panorama"):
    pass
else:
    os.system("mkdir "+tempfolder+"\panorama")
tempdir = tempfolder+"\panorama"
os.system("echo. >"+tempdir+"\panorama.html")
os.system("echo. >"+tempdir+"\usbdeview.html")
os.system("echo. >"+tempdir+"\prefetch.html")
os.system('type "' + os.getcwd() + '\sources\logo.png" >> '+tempdir+'\logo.png"')
os.system('type "' + os.getcwd() + '\sources\soundplay.wav" >> '+tempdir+'\soundplay.wav"')

ifcanrun = 1

class fromhostget():
    def __init__(self):
        self.hostname = str(os.popen('hostname').read().split()[0]) # Called by fromhostget().hostname

    # Audio test (Sound and Record):
    def soundtest(self):
        played = 0
        recorded = 0

        # Play:
        runonrun = 0 # do test sound also when running?
        if runonrun == 1:
            try: 
                wf = wave.open(tempdir+"\soundplay.wav", 'rb')
                p = pyaudio.PyAudio()
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), output=True)
                data = wf.readframes(1024)
                while data != '':
                    stream.write(data)
                    data = wf.readframes(1024)

                stream.stop_stream()
                stream.close()

                p.terminate()
                played = 1
            except: # If there is excption so there is no output
                played = 0

        # Record:
        try: 
            RECORD_SECONDS = 7
            WAVE_OUTPUT_FILENAME = tempdir+"\soundrecord.wav"
            audio = pyaudio.PyAudio()
            
            stream = audio.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)
            frames = []
            for i in range(0, int(44100 / 1024 * RECORD_SECONDS)):
                frames.append(stream.read(1024))

            # STOP Recording:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')            
            waveFile.setnchannels(2)
            waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            waveFile.setframerate(44100)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
            recorded = 1
        except: # If there is excption so there is no input
            recorded = 0

        return recorded, played

    # Operating system:
    def os(self):
        try: # Extract the windows dist name
            explorer = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            osver = (str(_winreg.QueryValueEx(explorer, 'ProductName')[0]).encode('utf-8').decode('utf-8'))
        except:
            osver = "Windows UNKNOWN"

        try: # Extract the windows service pack
            explorer = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SYSTEM\CurrentControlSet\Control\Windows")
            ossp = (str(_winreg.QueryValueEx(explorer, 'CSDVersion')[0]).encode('utf-8').decode('utf-8'))
            if ossp == "256":
                ossp = "SP1"
            elif ossp == "512":
                ossp = "SP2"
            elif ossp == "768":
                ossp = "SP3"
            elif ossp == "1024":
                ossp = "SP4"
            else:
                ossp = "SP1"
        except:
            ossp = "SP1"

        try: # Check if 64Bit or 32Bit
            explorer = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
            osarch = (str(_winreg.QueryValueEx(explorer, 'PROCESSOR_ARCHITECTURE')[0]).encode('utf-8').decode('utf-8'))
            if "86" not in osarch:
                osarch = "x64"
        except:
            osarch = "x86"

        try: # Extract install date
            explorer = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            osidate = (str(_winreg.QueryValueEx(explorer, 'InstallDate')[0]).encode('utf-8').decode('utf-8'))
            if len(osidate) < 5:
                osidate = os.popen('systeminfo | find "Original Install Date"').read().split("Date:")[1].strip()
            else:
                osidate = datetime.datetime.fromtimestamp(int(osidate)).strftime('%d/%m/%Y')
        except:
            osidate = "00000"

        # One and full OS name:
        fullos = osver+" "+ossp+" "+osarch

        oswords = fullos.split()

        # ifcanrun = 0 - means that this OS not have firewall, wmic, windows updates etc...
        global ifcanrun
        if "XP" in oswords and "SP1" in oswords:
            ifcanrun = 0
        if "95" in oswords or "98" in oswords or "2000" in oswords:
            ifcanrun = 0

        return osver, ossp, osarch, fullos, osidate

    # Manufacturer serial number:
    def serialnumber(self):
        global ifcanrun
        if ifcanrun == 1:
            try:
                return os.popen("wmic bios get serialnumber").read().split("\n")[1]
            except:
                return "N/A"
        else:
            return "N/A"

    # Firewall - status and allowed apps:
    def firewall(self):
        global ifcanrun
        if ifcanrun == 1: # If not can run so no firewall for this windows
            try: # Check if firewall is on or off:
                output = os.popen("netsh advfirewall show allprofiles state").read()
                if "OFF" in output:
                    firewall = 0
                else:
                    firewall = 1
            except:
                firewall = 0

            # Collecting allowed applications:
            rules = {}
            try:
                explorer = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SYSTEM\CurrentControlSet\services\SharedAccess\Parameters\FirewallPolicy\FirewallRules")
                count = 0
                nodata = 0
                while nodata < 3: 
                    try:
                        name, value, type = _winreg.EnumValue(explorer, count)
                        if "Allow" in value and "TRUE" in value:
                            nodata = 0
                            app = value.split("App=")[1].split("|Name")[0]
                            name = value.split("Name=")[1].split("|")[0]

                            if app != "System" and app not in rules:
                                if "FirewallAPI.dll" not in name:
                                    if "%SystemRoot%\system32\svchost.exe|" not in app:
                                        rules[name]=app
                    except:
                        nodata += 1
                    count += 1
            except:
                pass
        else:
            firewall = 0
            rules = {}

        return firewall, rules

    # Hotfixes (Windows updates):
    def hotfixs(self):
        global ifcanrun
        if ifcanrun == 1:
            try:
                kblist = str(os.popen("wmic qfe get hotfixid,installedon").read()).split("\n")
                kb_list = {}
                hotfixCount = 0
                for i in kblist:
                    if i[:2] == "KB":
                        hotfixCount += 1
                        kbname,date = i.split()
                        if date in kb_list:
                            kb_list[date].append(kbname)
                        else:
                            kb_list[date] = []
                            kb_list[date].append(kbname)
                
                return kb_list, hotfixCount
            except:
                return [],0

        else:
            return [],0

    # McAfee settings and logs:
    def mcafee(self):
        try:
            # Version:
            explorer = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"Software\McAfee\DesktopProtection")
            mcafeever = (str(_winreg.QueryValueEx(explorer, 'szProductVer')[0]).encode('utf-8').decode('utf-8'))

            # Dat date:
            try:
                explorer = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"Software\McAfee\AVEngine")
                signdate = ((str(_winreg.QueryValueEx(explorer, 'AVDatDate')[0]).encode('utf-8').decode('utf-8'))).split("/")
                signdate = signdate[2]+"/"+signdate[1]+"/"+signdate[0]
            except:
                signdate = "10/10/10"

            # Action mode:
            try:
                explorer = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"Software\McAfee\SystemCore\vscore\On Access Scanner\McShield\Configuration\Default")
                avmode = (str(_winreg.QueryValueEx(explorer, 'uAction_Program')[0]).encode('utf-8').decode('utf-8'))
                avmode2 = (str(_winreg.QueryValueEx(explorer, 'uAction')[0]).encode('utf-8').decode('utf-8'))
                if avmode == "4" or avmode == "5" or avmode2 == "4" or avmode2 == "5":
                    avmode = "delete"
                else:
                    avmode = "scan"
            except:
                avmode = "delete"

            # Automatic scan:
            try:
                explorer = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"Software\Wow6432Node\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}")
                if (str(_winreg.QueryValueEx(explorer, 'bSchedEnabled')[0]).encode('utf-8').decode('utf-8')) == "1" and (str(_winreg.QueryValueEx(explorer, 'Weekly_maskDaysOfWeek')[0]).encode('utf-8').decode('utf-8')) != "0":
                    avweek = 1
                else:
                    avweek = 0
            except:
                explorer = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"Software\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}")
                if (str(_winreg.QueryValueEx(explorer, 'bSchedEnabled')[0]).encode('utf-8').decode('utf-8')) == "1" and (str(_winreg.QueryValueEx(explorer, 'Weekly_maskDaysOfWeek')[0]).encode('utf-8').decode('utf-8')) != "0":
                    avweek = 1
                else:
                    avweek = 0

            # Get log dir path:
            try:
                explorer = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"System\CurrentControlSet\Control\Session Manager\Environment")
                path = (str(_winreg.QueryValueEx(explorer, 'DEFLOGDIR')[0]).encode('utf-8').decode('utf-8'))
            except:
                path = "C:\ProgramData\McAfee\DesktopProtection"

            # Looking for intersing logs on logs files:
            events = []
            filenames = ['AccessProtectionLog.txt','OnAccessScanLog.txt','OnDemandScanLog.txt']
            for logfile in filenames:
                try:
                    logfile = open(path+"\\"+logfile,'r').read()
                    for line in logfile.split("\n"):
                        if "(Trojan)" in line or "(Virus)" in line or "Deleted" in line or "No Action Taken" in line:
                            if "(scan timed out)" not in line:
                                events.append(line)
                    logfile.close()
                except:
                    pass

            # Last scan date:
            offset = 0
            line = ''
            try:
                with open(path+"\\"+"OnDemandScanLog.txt") as f: 
                    while True: 
                        offset -= 1 
                        f.seek(offset, 2) 
                        nextline = f.next() 
                        if nextline == '\n' and line.strip(): 
                            lastscan = line.split("\t")[0]+" - "+line.split("\t")[1]
                            break
                        else: 
                            line = nextline
                if len(lastscan) < 5:
                    lastscan = "0"
            except:
                lastscan = "0"

            # McAfee Exclutions:
            avcexclutions = []
            try:
                count = 0
                nodata = 0
                while nodata < 3:
                    try:
                        try:
                            name, value, type = _winreg.EnumValue(_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Wow6432Node\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}"), count)
                        except:
                            name, value, type = _winreg.EnumValue(_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\McAfee\DesktopProtection\Tasks\{21221C11-A06D-4558-B833-98E8C7F6C4D2}"), count)
                        if name[:11] in "ExcludedItem_":
                            avcexclutions.append(value)
                        nodata = 0
                    except:
                        nodata = nodata + 1
                    count += 1
            except:
                pass

            # Quarantine files:
            qtnfiles = []
            if os.path.exists('C:/quarantine'):
                for a in os.listdir('C:/quarantine'):
                    qtnfiles.append(a)

            return mcafeever,signdate,avmode,avweek,path,events,lastscan,avcexclutions, qtnfiles # mcafeever,mcafeesigndate,mcafeemode,mcafeeweek,mcafeelogpath = fromhostget().mcafee()
        except:
            return

    # Looking for WiFi cards:
    def wireless(self):
        morewireless = []
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkCards", 0, _winreg.KEY_READ)
        for i in xrange(0, _winreg.QueryInfoKey(key)[0]):
            try:
                skey_name = _winreg.EnumKey(key, i)
                skey = _winreg.OpenKey(key, skey_name)
                cardname = str(_winreg.QueryValueEx(skey, 'Description')[0]).encode('utf-8').decode('utf-8')
                morewireless.append(cardname)
            except:
                pass
        return morewireless

    # Getting prefetch files (Also ask for admin permissions):
    def prefetch(self):
        os.system("sources\winprefetchview.exe /stext "+tempfolder+"\panorama\prefetch.html")
        prefetchhtml = tempfolder+"\panorama\prefetch.html"
        prefetchhtmlread = open(prefetchhtml,'r').read().decode('utf-16')
        return prefetchhtmlread

    # Parsing and building USB dictionary:
    def usbdeview(self):
        os.system("sources\USBDeview.exe /shtml "+tempfolder+"\panorama\usbdeview.html")
        networds = ['wireless','lan','bluetooth','ethernet','802.11','nic','802.11n','802.11a','802.11ac','802.11g','802.11b','net','tplink','tp-link','linksys','dlink','d-link','link','band','ac','dualband','dsl','netstick']
        files = tempfolder+"\panorama\usbdeview.html"
        usbdfile = open(files,'r').read().split("<tr>")
        usbs = {}
        detectedWireless = []
        uid = 0
        for usb in usbdfile:
            try:
                if "<td" == usb[:3]:
                    uid = uid + 1
                    usbs[uid]={}
                    #get all values from table:
                    usbparse = re.findall(r"([^>]*)[$<]", usb)
                    #get the usb title:
                    if "0000" in usbparse[1]:
                        usbname = usbparse[2]
                    else:
                        usbname=usbparse[1]+" - "+usbparse[2]
                    for word in usbname.replace("_"," ").split():
                        if word in networds:
                            if usbname not in detectedWireless:
                                detectedWireless.append(usbname)
                    usbs[uid]['name']=usbname
                    #get the usb type:
                    usbtype = usbparse[3]
                    usbs[uid]['type']=usbtype
                    #get the usb serial:
                    usbserial = usbparse[9]
                    usbs[uid]['serial']=usbserial
                    #get the first date:
                    usbfdate = usbparse[10]
                    usbs[uid]['fdate']=usbfdate.replace(" ","|")
                    #get the last date:
                    usbldate = usbparse[11]
                    usbs[uid]['ldate']=usbldate.replace(" ","|")
            except:
                pass

        for card in self.wireless(): # Check for more wireless cards
            try:
                if card not in detectedWireless and 'wireless' in card.lower().split():
                    detectedWireless.append(card)
            except:
                pass
        return usbs,detectedWireless # usbs,detectedWireless = fromhostget().usbdeview()

    # Getting users info:
    def usersinfo(self):
            netuser = os.popen('net user').read().split("\n")
            highusers = []
            lowusers = []
            users = ""
            for line in netuser:
                try:
                    if line[:2] != "" and line[:1] != "-" and "User accou" not in line and "The command" not in line:
                        users += line+"            "
                except:
                    pass
            for user in users.split():
                netname = os.popen('net user '+user).read()
                if 'Administrators' in netname:
                    try:
                        highusers.append(str(user).encode('utf-8'))
                    except:
                        # print "Notice 325: Skipped Hebrew username."
                        pass
                else:
                    try:
                        lowusers.append(str(user).encode('utf-8'))
                    except:
                        # print "Notice 423: Skipped Hebrew username."
                        pass
            return highusers,lowusers # highusers,lowusers = fromhostget().usersinfo()

    # All installed softwares:
    def softwares(self):
        installedsoftwares = set()
        # Getting installed softwares from SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall:
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, _winreg.KEY_READ)
        for i in xrange(0, _winreg.QueryInfoKey(key)[0]):
            try:
                skey_name = _winreg.EnumKey(key, i)
                skey = _winreg.OpenKey(key, skey_name)
                try:
                    softname = str(_winreg.QueryValueEx(skey, 'DisplayName')[0]).encode('utf-8').decode('utf-8')
                    installedsoftwares.add(softname)
                except:
                    pass
                finally:
                    skey.Close()
            except:
                pass

        # Dir names at Program Files:
        for dirs in (os.walk('C:\Program Files')):
            for dirname in (dirs[1]):
                if dirname not in installedsoftwares:
                    installedsoftwares.add(dirname)
            break

        # Dir names at Program Files x86:
        for dirs in (os.walk('C:\Program Files (x86)')):
            for dirname in (dirs[1]):
                if dirname not in installedsoftwares:
                    try:
                        installedsoftwares.add(dirname)
                    except:
                        pass
            break
        
        # Dir names at AppData:
        appdata = os.popen('echo %AppData%').read()
        for dirs in (os.walk(str(appdata.split("\n")[0]))):
            for dirname in (dirs[1]):
                if dirname not in installedsoftwares:
                    try:
                        installedsoftwares.add(dirname)
                    except:
                        pass
            break

        return installedsoftwares

    # IP Address:
    def ips(self):
        ipdict = {}
        try:
            # Getting IPs and dates from registry ...parameters\interfaces:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"System\CurrentControlSet\services\Tcpip\parameters\interfaces", 0, _winreg.KEY_READ)
            for i in xrange(0, _winreg.QueryInfoKey(key)[0]):
                try:
                    skey_name = _winreg.EnumKey(key, i)
                    skey = _winreg.OpenKey(key, skey_name)
                    ipadd = str(_winreg.QueryValueEx(skey, 'DhcpIPAddress')[0]).encode('utf-8').decode('utf-8')
                    ipdate = str(_winreg.QueryValueEx(skey, 'LeaseObtainedTime')[0]).encode('utf-8').decode('utf-8')
                    ipdate = datetime.datetime.fromtimestamp(int(ipdate)).strftime('%d/%m/%Y')
                    if ipadd == "0.0.0.0":
                        pass
                    else:
                        ipdict[ipadd] = ipdate
                except:
                    pass
        except:
            pass

        try:
            # Getting current IP Addresses:
            getCurrentIPs = os.popen('ipconfig | find "IPv4"').read().split("\n")
            if len(getCurrentIPs) < 5:
            	getCurrentIPs = os.popen('ipconfig | find "IP"').read().split("\n")
            for ip in getCurrentIPs:
                try:
                    ipdict[ip.split(":")[1].strip()] = "now"
                except:
                    pass
        except:
            pass
        return ipdict #Called by fromhostget().ips()

    # Physical address:
    def macs(self):
        macs = []
        getmacs = os.popen('ipconfig /all | find "Physical Address"').read().split("\n")
        for addr in getmacs:
            try:
                macs.append(addr.split(":")[1].strip())
            except:
                pass
        return macs

    # Network status (open connections):
    def netstat(self):
        netstat = os.popen("netstat -no").read()
        ports = {}
        for each in netstat.split("\n"):
            try:
                if "tcp" in each.lower() or "udp" in each.lower():
                    port = each.split("  ")
                    info = []
                    for inf in port:
                        if inf != '':
                            info.append(inf)
                    protocol = str(info[0]).strip()
                    source = str(info[1]).strip()
                    target = str(info[2]).strip()
                    status = str(info[3]).strip()
                    pid = str(info[4]).strip()

                    ports[pid]={}
                    ports[pid]['protocol']=protocol
                    ports[pid]['source']=source
                    ports[pid]['target']=target
                    ports[pid]['status']=status
            except:
                pass
        return ports

    # Commands on startup:
    def startup(self):
        startupcommands = []
        # Getting commands on startup from registry ...CurrentVersion\Run:
        explorer = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        count = 0
        nodata = 0
        while nodata < 3: 
            try:
                name, value, type = _winreg.EnumValue(explorer, count)
                nodata = 0
                if "mcafee" in value.lower():
                    pass
                else:
                    startupcommands.append(value)
            except:
                nodata += 1
            count += 1

        # Getting commands on startup from registry ...CurrentVersion\RunOnce:
        explorer = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce")
        count = 0
        nodata = 0
        while nodata < 3: 
            try:
                name, value, type = _winreg.EnumValue(explorer, count)
                if "mcafee" in value.lower():
                    pass
                else:
                    startupcommands.append(value)
            except:
                nodata += 1
            count += 1
        return startupcommands

    # Task scheduler:
    def tasks(self):
        tasks = {}
        try:
            getAllTasks = os.popen("schtasks").read().split("Folder: ")
            for each in getAllTasks:
                try:
                    if each[1:10] != "Microsoft":
                        for task in each.split("\n")[3:]:
                            taskvalue = task.split("    ")
                            taskvalue[0] = taskvalue[0].replace(" ","")
                            taskvalue[1] = taskvalue[1].replace(" ","")
                            taskvalue[2] = taskvalue[2].replace(" ","")
                            taskvalue = ' '.join(taskvalue).split()
                            tasks[taskvalue[0]] = taskvalue[1]
                except:
                    pass
            return tasks
        except:
            return tasks

    # Running proccess:
    def processes(self):
        # whitelist = ["audiodg.exe","conhost.exe","csrss.exe","lsass.exe","lsm.exe","MSCamS64.exe","McTray.exe","alg.exe","naPrdMgr.exe","OSPPSVC.EXE","PresentationFontCache.exe","SearchIndexer.exe","services.exe","smss.exe","spoolsv.exe","svchost.exe","System","SystemIdleProcess","UNS.exe","wininit.exe","WmiApSrv.exe","WmiPrvSE.exe","wmpnetwk.exe","WUDFHost.exe","chrome.exe","atiesrxx.exe","stacsv64.exe","tasklist.exe","conhost.exe","SmartMenu.exe","explorer.exe","explore.exe","taskhost.exe","cmd.exe","LogonUI.exe","jusched.exe","dllhost.exe","taskeng.exe","TrustedInstaller.exe","shstat.exe","winlogon.exe","ctfmon.exe","mcshield.exe","WLIDSVC.EXE","notepad.exe","VsTskMgr.exe","mfeann.exe","RtkNGUI64.exe","mfevtps.exe"]
        processes = {}
        try:
            getAllProcesses = os.popen("tasklist /svc /fo CSV").read().split("\n")[3:]
            for each in getAllProcesses:
                try:
                    proc = each.split('","')
                    # if proc[0] in whitelist:
                    #     pass
                    # else:
                    processes[proc[0].replace('"','')] = [proc[1].replace('"',''), str(proc[2]).replace('"','')]
                except:
                    pass
            return processes
        except:
            return processes

def writehtml():
    html = open(tempdir+"\panorama.html",'w')
    ###########################################
    # General:#################################
    ###########################################
    html.write("""<html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <html>
    <head>
      <title>Panorama - Fast incident overview</title>
    <style>
        body {
            background-color: #072144;
            max-width: 100%;
            margin: 0;
            padding-top: 15px;
            margin-left: auto;
            margin-right: auto;
            font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif;m,
        }
        ul.tab {
            list-style-type: none;
            margin: 0;
            padding: 0;
            overflow: hidden;
            border: 1px solid #ccc;
            background-color: #d2d2d2;
            width: 100%;
        }
        ul.tab li {
            float: left;
        }
        ul.tab li a {
            display: inline-block;
            color: #072144;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
            transition: 0.3s;
            font-size: 17px;
        }
        ul.tab li a:hover a:focus, .active {
            background-color: #7f7f7f;
            -webkit-border-radius: 10px;
            -moz-border-radius: 10px;
            border-radius: 10px;
        }
        .tabcontent {
            display: none;
            -webkit-animation: fadeEffect 1s;
            animation: fadeEffect 1s;
        }
        @-webkit-keyframes fadeEffect {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        @keyframes fadeEffect {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        .title {
            font-weight: bold;
            font-size: 35px;
            margin-bottom: 3px;
        }
        .title-all {
            width: 200px;
            height: 17px;
            border-radius: 15px;
            -webkit-border-radius: 15px;
            -moz-border-radius: 15px;
            background-color: #ADADAD;
            margin-top: 0px;
            float: left;
        }
        a {
            text-decoration: none;
            color: #fff;
        }
        a:hover{
            text-decoration: underline;
            color: #fff;
        }
        table {
            border-collapse: collapse;
            margin-right: auto;
        }
        th, td {
            text-align: left;
            padding: 8px;
        }
        tr {
         background-color: #dedede;
        }
        tr:nth-child(even){
        background-color: #f2f2f2
        }
        tr:hover {
         background-color: #bbbbbb;
        }
        hr {
            max-width: 60%;
        }
        .white {
            width: 100%;
            background-color: #fff;
            color: #072144;
        }
        .blue {
            width: 100%;
            background-color: #072144;
            color: #ffffff;
        }
        .content {
            width: 80%;
            margin-left: auto;
            margin-right: auto;
            padding-top: 25px;
            padding-bottom: 25px;
        }
    </style>
    </head>
    <body>
    <script>
        function opentab(evt, tabName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
    </script>""")

    html.write('<div style="width: 80%;"><div style="float: left;"><img src="'+tempdir+'\logo.png"></div><div style="float: right; width: 50%; color: #fff; padding-top: 20;">')
    html.write('<b>Hostname: </b>{}<br>'.format(hostname))
    html.write('<b>Serial number: </b>{}<br>'.format(serialnumber))
    html.write('<b>OS: </b>{}<br>'.format(fullos))
    html.write('<b>Install date: </b>{}<br>'.format(osidate))
    html.write('<b>Updates number: </b>{}<br>'.format(str(hotfixCount)))

    if firewall == 1:
        html.write('<b>Firewall: </b><b>ON</b><br>')
    else:
        html.write('<b>Firewall: </b><b>OFF</b>')

    html.write("""</div></div><div style="clear: both;"></div><br>
        <ul class="tab">
        <li><a href="#" class="tablinks" onclick="opentab(event, 'software')">Software</a></li>
        <li><a href="#" class="tablinks" onclick="opentab(event, 'security')">Security</a></li>
        <li><a href="#" class="tablinks" onclick="opentab(event, 'networking')">Networking</a></li>
        <li><a href="#" class="tablinks" onclick="opentab(event, 'general')">General</a></li>
        </ul>""")


    # Starting write the tab contents:
    ###########################################
    ################ SECURITY: ################
    html.write('<div id="security" class="tabcontent">')
    # Firewall Rules ##########################
    ###########################################
    html.write('<div class="white"><div class="content"><div class="title">Allowed applications on firewall:</div>')
    if len(firewallrules) > 0:
        html.write("<table><tr><td><b>Name</b></td><td><b>Path</b></td></tr>")
        for name,rule in firewallrules.iteritems():
            html.write("<tr><td>"+name+"</td><td>"+rule+"</td></tr>")
        html.write("</table>")

    else:
        html.write("<b>No applications allowed on firewall</b></br>")
    html.write('</div></div>')
    # McAfee ##################################
    ###########################################
    html.write('<div class="blue"><div class="content"><div class="title">McAfee: </div>')
    if mcafee:
        mcafeever,mcafeesigndate,mcafeemode,mcafeeweek,mcafeelogpath,mcafeeevents,mcafeelastscan,avcexclutions, quarantine = mcafee
        html.write('<b>Version: </b>{}<br>'.format(mcafeever))
        html.write('<b>Dat date: </b>{}<br>'.format(mcafeesigndate))
        if mcafeemode == "delete":
            html.write('<b>Action mode: </b>Delete<br>')
        else:
            html.write('<b>Action mode: </b>Scan<br>')

        if mcafeeweek == 1:
            html.write('<b>Weekly scan: </b>Yes<br>')
        else:
            html.write('<b>Weekly scan: </b>No<br>')

        if mcafeelastscan == "0":
            html.write('<b>Last scan date: </b>Never<br>')
        else:
            html.write('<b>Last scan date: </b>{}<br>'.format(mcafeelastscan))

        html.write("<br><b>Exclusions:</b><br>")
        if len(avcexclutions) == 0:
            html.write('No exclusions<br>')
        else:
            for role in avcexclutions:
                if role[0] == "3":
                    html.write("• Not scanner file: "+role.rsplit("|",1)[1]+'<br>')
                elif role[0] == "4":
                    html.write("• Not scanner format: "+role.rsplit("|",1)[1]+'<br>')
                elif role[0] in ["0","2"]:
                    html.write("• Not scanner files older than "+role.rsplit("|",1)[1]+' days<br>')
                elif role[0] == "1":
                    html.write("• No scanner files that unused more than "+role.rsplit("|",1)[1]+' days<br>')
                else:
                    html.write(role+"<br>")

        # Quarantine:
        html.write("<br><b>Quarantine Folder:</b><br>")
        if len(quarantine) == 0:
            html.write("No files in quarantine folder<br>")
        else:
            html.write("Found "+str(len(quarantine))+" files:<br>")
            for each in quarantine:
                html.write(each+"<br>")

        # Logs:
        html.write("<br><b>Logs:</b><br>")
        if len(mcafeeevents) == 0:
            html.write("Not interesting logs<br>")
        else:
            html.write("<table><tr><td><b>Date</b></td><td><b>Action</b></td><td><b>File</b></td><td><b>Signature</b></td><td><b>MD5</b></td></tr>")
            for log in mcafeeevents:
                log = log.split("\t")
                action = log[2]
                html.write(
                    "<tr><td>"+log[0]+" - "+log[1]+"</td>"+
                    "<td>"+action+"</td>"+
                    "<td>"+log[5]+"</td>"+
                    "<td>"+log[6].replace(")","").replace("(","- ")+"</td>")
                try:
                    html.write("<td>"+log[7].replace(")","").replace("(","- ").split(" ")[0]+"</td>")
                except:
                    html.write("<td></td>")

        html.write("</tr></table><br><b>Log files:</b><br>")
        logfiles = []
        for (dirpath, dirnames, filenames) in os.walk(mcafeelogpath):
            logfiles.extend(filenames)
            break
        for log in logfiles:
            if log[-3:] != 'bak':
                html.write('<a target="_blank" href="{}\{}">{}</a><br>'.format(mcafeelogpath,log,log))
    else:
        html.write("McAfee is not installed</br>")
    html.write('</div></div>')

    # Hotfixs ##################################
    ############################################
    html.write('<div class="white"><div class="content"><div class="title">Windows security updates:</div>')
    try:
        if hotfixCount == 0:
            html.write("<b>No updates installed!</b>")
        else:
            for date,kblist in hotfixs.iteritems():
                html.write("Packages installed on <b>{}</b>: <br>".format(date))
                html.write((", ".join(str(x) for x in kblist))+"<br><br>")
    except:
        html.write("<b>No updates installed!</b>")
    html.write('</div></div>')

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    html.write('</div>')
    ############# END SECURITY ################
    ###########################################




    ###########################################
    ############## NETWORKING: ################
    html.write('<div id="networking" class="tabcontent">')
    # IPS #####################################
    ###########################################
    html.write('<div class="white"><div class="content"><div class="title">IP and MAC address: </div>')

    html.write('<br><b>IP Address:</b>')
    if len(ips) == 0:
        html.write("<br>IP never has use")
    else:
        for ip,date in ips.iteritems():
            if date == "now":
                html.write("<br>Current IP address: "+str(ip)+"")
        for ip,date in ips.iteritems():    
            if date != "now":
                html.write("<br>IP: "+str(ip)+" Date: "+str(date)+"")
    
    html.write('<br><br><b>MAC Address:</b><br>')
    if len(macs) == 0:
        html.write("Network card not connected<br>")
    else:
        for add in macs:
            if add[:11] != "00-00-00-00":
                html.write(add+"<br>")
    html.write('</div></div>')

    # NETSTAT #################################
    ###########################################
    html.write('<div class="blue"><div class="content"><div class="title">Network status: </div>')
    html.write('<font face="Arial"><table style="width:85%"><tr><td><b>Source</b><td><b>Target</b><td><b>Protocol</b><td><b>PID</b><td><b>Status</b></tr>')
    for proc in netstat:
        html.write("<tr><td>"+netstat[proc]['source'][:28]+"</td><td>"+netstat[proc]['target'][:28]+"</td><td>"+netstat[proc]['protocol']+"</td><td>"+proc+"</td><td>"+netstat[proc]['status']+"</td></tr>")
    html.write("</table>")
    html.write('</div></div>')

    # WIRELESS ################################
    ###########################################
    html.write('<div class="white"><div class="content"><div class="title">WiFi Connections: </div>')
    if len(detectedWireless) >= 1:
        for card in detectedWireless:
            html.write("<br><b>Wireless card: "+str(card)+"</b><br>")
    else:
        html.write("Never connected Wi-Fi device")
    html.write('</div></div>')

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    html.write('</div>')
    ########### END NETWORKING ################
    ###########################################




    ###########################################
    ############### SOFTWARE: #################
    html.write('<div id="software" class="tabcontent">')
    # STARTUP #################################
    ###########################################
    html.write('<div class="white"><div class="content"><div class="title">Commands on startup:</div>')
    if len(startup) == 0:
        html.write("No commands on startup<br><br>")
    else:
        for command in startup:
            html.write("• "+command+"<br>")
    html.write('</div></div>')

    # SCHTASKS ################################
    ###########################################
    html.write('<div class="blue"><div class="content"><div class="title">Task scheduler:</div>')
    if len(tasks) == 0:
        html.write("There are no scheduled tasks<br><br>")
    else:
        html.write('<center><font face="Arial"><table style="width:75%"><tr><td><b>Task name</b><td><b>Execution date</b></tr>')
        for task,date in tasks.iteritems():
            if date == "Ready":
                date = "N/A"
            if date == "N/A":
                html.write("<tr><td>"+task+"</td><td>No date</td></tr>")
            else:
                html.write("<tr><td>"+task+"</td><td>"+date+"</td></tr>")
        html.write("</table></center>")
    html.write('</div></div>')

    # PREFETCH ################################
    ###########################################
    html.write('<div class="white"><div class="content"><div class="title">Prefetch:</div>')
    table = """<table><tr>
                <td><b>Filename</b></td>
                <td><b>Created Time</b></td>
                <td><b>Modified Time</b></td>
                <td><b>File Size</b></td>
                <td><b>Process EXE</b></td>
                <td><b>Process Path</b></td> 
                <td><b>Run Counter</b></td>
                <td><b>Last Run Time</b></td>
                <td><b>Missing Process</b></td></tr><tr>"""
    html.write(table)
    count = 0
    linesname = ["Filename", "Created", "Modified", "File", "Process", "Process", "Run", "Last", "Missing"]
    for line in prefetch.split("\n"):
        if "===" in line or line.strip().replace(" ","") == "" or len(line) == 0:
            pass
        else:
            if line.split(" ")[0] in linesname:
                html.write("<td>"+line.split(":")[1]+"</td>")
                count += 1
        if count == 9:
            count = 0
            html.write("</tr><tr>")
    html.write("</tr></table></div></div>")

    # ACTIVE PROCESS ##########################
    ###########################################
    html.write('<div class="blue"><div class="content"><div class="title">Process list:</div>')

    if len(processes) == 0:
        html.write("No processes<br><br>")
    else:
        html.write('<center><font face="Arial"><table style="width:75%"><tr><td><b>Name</b></td><td><b>PID</b></td><td>Description</td></tr>')
        for proc,pid in processes.iteritems():
            html.write("<tr><td>"+proc+"</td><td>"+pid[0]+"</td><td>"+str(pid[1])+"</td></tr>")
        html.write("</table></center>")
    html.write('</div></div>')

    # INSTALLED ###############################
    ###########################################
    html.write('<div class="white"><div class="content"><div class="title">Installed Softwares:</div>')
    for soft in sorted(installedsoftwares):
        html.write("• "+soft+"<br>")
    html.write('</div></div>')

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    html.write('</div>')
    ############# END SOFTWARE ################
    ###########################################




    ###########################################
    ############### GENERAL: ##################
    html.write('<div id="general" class="tabcontent">')
    # USERS ###################################
    ###########################################
    html.write('<div class="white"><div class="content"><div class="title">Users:</div>')
    html.write('<b>Administrators: </b><br>')
    count = 1
    for admin in highusers:
        html.write(str(count)+". "+admin+"<br>")
        count += 1
    count = 1
    html.write('<br><b>Low Users: </b><br>')
    for regular in lowusers:
        html.write(str(count)+".  "+regular+"<br>")
        count += 1
    html.write('</div></div>')

    # USBS ####################################
    ###########################################
    html.write('<div class="blue"><div class="content"><div class="title">USB Connections:</div>')
    networds = ['wireless','lan','bluetooth','ethernet','802.11','nic','802.11n','802.11a','802.11ac','802.11g','802.11b','net','tplink','tp-link','linksys','dlink','d-link','link','band','ac','dualband']
    storagewords = ['wd','sandisk','flash','kingston','toshiba','transcend','corsair','datatravel','portable','hitachi','jetflash','patriot','storage','floppy','generic','4gb','8gb','16gb','32gb','64gb','128gb','256gb']
    smartwords = ['android','iphone','ipod','apple','htc','dell','samsung','lg','ipad','galaxy','sony','note','tab','tablet','phone','budget','nokia','linux','gadget','black','blackberry','belkin','smart','nexus','oneplus','watch','motorola','google','huawei','g3','g4','acer','xbox','mobile','lumia','web','gt-i9100','gt-i9200','gt-i9300','gt-i9100t','sm-g900f','sm-g900i','sm-g900','sm-g920','sm-g920i','sm-g920f','windows', 'sm-g900f']
    camerawords = ['canon','camera','nikon','webcam','cam','powershot']
    license = ['safenet']
    cdrom = ['cddvd', 'dvdram', 'cdram']
    html.write("<table><tr><td><b>Name</b></td><td><b>Related</b></td><td><b>Type</b></td><td><b>Serial</b></td><td><b>Date</b></td></tr>")
    for x,usb in usbs.iteritems():
        try:
            namelower = usb['name'].lower()
            html.write('<tr><td>'+usb['name']+'</td><td>')
            for word in namelower.replace("_"," ").split(" "):
                related = 0
                if word in networds:
                    html.write("Network")
                    related = 1
                    break
                elif word in storagewords:
                    html.write("Disk-on-Key / External HardDrive")
                    related = 1
                    break
                elif word in smartwords:
                    html.write("Smartphone / Media Device")
                    related = 1
                    break
                elif word in camerawords:
                    html.write("Camera")
                    related = 1
                    break
                elif word in license:
                    html.write("License device")
                    related = 1
                    break
                elif word in cdrom:
                    html.write("External CD/DVD")
                    related = 1
                    break
            if related == 0:
                html.write("N/A")
            html.write("</td>")
            html.write('<td>'+usb['type']+'</td>')

            if usb['serial'] != "&nbsp;":
                html.write('<td>'+usb['serial']+'</td>')
            else:
                html.write('<td>N/A</td>')

            date = usb['ldate'].split("|")
            date = date[0] + " - " + date[1]
            html.write('<td>'+date+'</td></tr>')
            # To add the first date use: usb['fdate']
        except:
            pass
    html.write('</table>')
    html.write('<b><a href="'+tempdir+'/usbdeview.html" target="_blank">> Click here to open the full USBDeview table <</a></b>')
    html.write('</div></div>')

    # SoundTest ###############################
    ###########################################
    html.write('<div class="white"><div class="content"><div class="title">Audio (Sound and Record):</div>')
    
    html.write("<br><b>Record:</b><br>")
    if not recorded:
        html.write("Microphone not found<br>")
    else:
        html.write("<br><b>Attempted recording in operating, Check if successful recording. (Speakers needed).</b><br>")
        html.write('<embed width="230" height="45" src="'+tempdir+'\soundrecord.wav" autostart="0">')
        html.write('<br><a href="'+tempdir+'\soundrecord.wav" title="Direct link to the audio file">'+tempdir+'\soundrecord.wav</a>')

    html.write("<br><br><b>Sound:</b><br>")
    if not played:
        html.write("Speakers not found<br>")
    else:
        html.write('<embed width="230" height="45" src="'+tempdir+'\soundplay.wav" autostart="0">')
        html.write('<br><a href="'+tempdir+'\soundplay.wav" title="Direct link to the audio file">'+tempdir+'\soundplay.wav</a>')

    html.write('</div></div>')
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    html.write('</div>')
    ########### END GENERAL ###################
    ###########################################


    #Finish writing and closing HTML div and file:
    html.write('</div>')
    ###########################################
    # END ############################### END #
    ###########################################

    html.close()
    print "Opens the report..."
    webbrowser.open_new("file:///"+tempdir+"/panorama.html")


def writetextfile():
    html = open(tempdir+"\panorama.txt",'w')
    html.write("-- Panorama v1.0 --\nFast incident overview\nGithub page: https://github.com/AlmCo/Panorama\nWrited by Almog Cohen - almogcn@gmail.com\n\n")
    linewidth = 110
    ###########################################
    # Host details: ###########################
    ###########################################
    html.write('\n'+'-'*linewidth+'\n')
    html.write('Host details:')
    html.write('\n'+'-'*linewidth+'\n')
    html.write('Hostname: {}\n'.format(hostname))
    html.write('Serial number: {}\n'.format(serialnumber))
    html.write('OS: {}\n'.format(fullos))
    html.write('Install date: {}\n'.format(osidate))
    html.write('Updates number: {}\n'.format(str(hotfixCount)))

    if firewall == 1:
        html.write('Firewall: ON\n')
    else:
        html.write('Firewall: OFF\n')


    ###########################################
    ################ SECURITY: ################
    html.write('\n'+'-'*linewidth+'\n')
    html.write('Security')
    html.write('\n'+'-'*linewidth+'\n')
    # Firewall Rules ##########################
    ###########################################
    html.write('Allowed applications on firewall:\n')
    if len(firewallrules) > 0:
        for name,rule in firewallrules.iteritems():
            html.write("\tName: "+name+"  |  Path: "+rule+"\n")

    else:
        html.write("No applications allowed on firewall\n")

    # McAfee ##################################
    ###########################################
    html.write('\nMcAfee:\n')

    if mcafee:
        mcafeever,mcafeesigndate,mcafeemode,mcafeeweek,mcafeelogpath,mcafeeevents,mcafeelastscan,avcexclutions, quarantine = mcafee
        html.write('\tVersion: {}\n'.format(mcafeever))
        html.write('\tDat date: {}\n'.format(mcafeesigndate))
        if mcafeemode == "delete":
            html.write('\tAction mode: Delete\n')
        else:
            html.write('\tAction mode: Scan\n')

        if mcafeeweek == 1:
            html.write('\tWeekly scan: Yes\n')
        else:
            html.write('\tWeekly scan: No\n')

        if mcafeelastscan == "0":
            html.write('\tLast scan date: Never\n')
        else:
            html.write('\tLast scan date: {}\n'.format(mcafeelastscan))

        html.write("\tExclusions:\n")
        if len(avcexclutions) == 0:
            html.write('\t\tNo exclusions\n')
        else:
            for role in avcexclutions:
                if role[0] == "3":
                    html.write("\t\t• Not scanner file: "+role.rsplit("|",1)[1]+'\n')
                elif role[0] == "4":
                    html.write("\t\t• Not scanner format: "+role.rsplit("|",1)[1]+'\n')
                elif role[0] in ["0","2"]:
                    html.write("\t\t• Not scanner files older than "+role.rsplit("|",1)[1]+' days\n')
                elif role[0] == "1":
                    html.write("\t\t• No scanner files that unused more than "+role.rsplit("|",1)[1]+' days\n')
                else:
                    html.write("\t\t• "+role+"\n")

        # Quarantine:
        html.write("\tQuarantine Folder:\n")
        if len(quarantine) == 0:
            html.write("\t\tNo files in quarantine folder\n")
        else:
            html.write("\t\tFound "+str(len(quarantine))+" files:\n")
            for each in quarantine:
                html.write("\t\t\t"+each+"\n")

        # Logs:
        html.write("\tLogs:\n")
        if len(mcafeeevents) == 0:
            html.write("\n\tNot interesting logs\n")
        else:
            for log in mcafeeevents:
                log = log.split("\t")
                action = log[2]
                html.write("\t\tDate: " + str(log[0])+" - "+str(log[1])+" | Action: "+ str(action) +" | Signature: "+ str(log[6].replace(")","").replace("(","- ")) +" | File: "+ str(log[5]))
                try:
                    html.write(" | MD5: " + log[7].replace(")","").replace("(","- ").split(" ")[0]+"\n")
                except:
                    html.write("\n")

        html.write("\tLog files:\n")
        logfiles = []
        for (dirpath, dirnames, filenames) in os.walk(mcafeelogpath):
            logfiles.extend(filenames)
            break
        for log in logfiles:
            if log[-3:] != 'bak':
                html.write('\t\t{}\n'.format(mcafeelogpath+"\\"+log))
    else:
        html.write("\tMcAfee is not installed\n")

    # Hotfixs ##################################
    ############################################
    html.write('\nWindows security updates:\n')

    try:
        if hotfixCount == 0:
            html.write("\tNo updates installed!\n")
        else:
            for date,kblist in hotfixs.iteritems():
                html.write("\tPackages installed on {}: ".format(date))
                html.write((", ".join(str(x) for x in kblist))+"\n")
    except:
        html.write("\tNo updates installed!\n")

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    ############# END SECURITY ################
    ###########################################




    ###########################################
    ############## NETWORKING: ################
    html.write('\n'+'-'*linewidth+'\n')
    html.write('Networking:')
    html.write('\n'+'-'*linewidth+'\n')
    # IPS #####################################
    ###########################################
    html.write('IP and MAC address:\n')

    html.write('\tIP Address:\n')
    if len(ips) == 0:
        html.write("\t\tIP never has use\n")
    else:
        for ip,date in ips.iteritems():
            if date == "now":
                html.write("\t\tCurrent IP address: "+str(ip)+"\n")
        for ip,date in ips.iteritems():    
            if date != "now":
                html.write("\t\tIP: "+str(ip)+" Date: "+str(date)+"\n")
    
    html.write('\tMAC Address:\n')
    if len(macs) == 0:
        html.write("\t\tNetwork card not connected\n")
    else:
        for add in macs:
            if add[:11] != "00-00-00-00":
                html.write("\t\t"+add+"\n")

    # NETSTAT #################################
    ###########################################
    html.write('\nNetwork status:\n')

    for proc in netstat:
        html.write("\tSource: "+netstat[proc]['source'][:28]+" | Target: "+netstat[proc]['target'][:28]+" | Protocol: "+netstat[proc]['protocol']+" | PID: "+proc+" | Status: "+netstat[proc]['status']+"\n")

    # WIRELESS ################################
    ###########################################
    html.write('\nWiFi Connections:\n')

    if len(detectedWireless) >= 1:
        for card in detectedWireless:
            html.write("\tWireless card: "+str(card)+"\n")
    else:
        html.write("\tNever connected Wi-Fi device\n")

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    ########### END NETWORKING ################
    ###########################################




    ###########################################
    ############### SOFTWARE: #################
    html.write('\n'+'-'*linewidth+'\n')
    html.write('Software:')
    html.write('\n'+'-'*linewidth+'\n')
    # STARTUP #################################
    ###########################################
    html.write('Commands on startup:\n')
    if len(startup) == 0:
        html.write("No commands on startup\n")
    else:
        for command in startup:
            html.write("\t• "+command+"\n")

    # SCHTASKS ################################
    ###########################################
    html.write('\nTask scheduler:\n')

    if len(tasks) == 0:
        html.write("There are no scheduled tasks\n")
    else:
        for task,date in tasks.iteritems():
            if date == "Ready":
                date = "N/A"
            if date == "N/A":
                html.write("\tTask: "+task+" | Execution date: No date\n")
            else:
                html.write("\tTask: "+task+" | Execution date: "+date+"\n")

    # PREFETCH ################################
    ###########################################
    html.write('\nPrefetch:\n')

    html.write("\t")
    newline = 1
    for line in prefetch.split("\n"):
        if line.strip().replace(" ","") == "" or len(line) == 0:
            pass
        elif "===" in line:
            if newline == 1:
                newline = 0
            else:
                html.write("\n\t")
                newline = 1
        else:
            html.write(line.replace("     "," ") + " | ")

    # ACTIVE PROCESS ##########################
    ###########################################
    html.write('\nProcess list:\n')

    if len(processes) == 0:
        html.write("\tNo processes\n")
    else:
        for proc,pid in processes.iteritems():
            html.write("\tName: "+proc+" | PID: "+pid[0]+" | Description: "+str(pid[1])+"\n")


    # INSTALLED ###############################
    ###########################################
    html.write('\nInstalled Softwares:\n')

    for soft in sorted(installedsoftwares):
        html.write("\t • "+soft+"\n")

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    ############# END SOFTWARE ################
    ###########################################




    ###########################################
    ############### GENERAL: ##################
    html.write('\n'+'-'*linewidth+'\n')
    html.write('General:')
    html.write('\n'+'-'*linewidth+'\n')
    # USERS ###################################
    ###########################################
    html.write('Users:\n')
    html.write('\tAdministrators: \n')
    count = 1
    for admin in highusers:
        html.write("\t\t"+str(count)+". "+admin+"\n")
        count += 1
    count = 1
    html.write('\tLow Users:\n')
    for regular in lowusers:
        html.write("\t\t"+str(count)+".  "+regular+"\n")
        count += 1

    # USBS ####################################
    ###########################################
    html.write('\nUSB Connections:\n')

    networds = ['wireless','lan','bluetooth','ethernet','802.11','nic','802.11n','802.11a','802.11ac','802.11g','802.11b','net','tplink','tp-link','linksys','dlink','d-link','link','band','ac','dualband']
    storagewords = ['wd','sandisk','flash','kingston','toshiba','transcend','corsair','datatravel','portable','hitachi','jetflash','patriot','storage','floppy','generic','4gb','8gb','16gb','32gb','64gb','128gb','256gb']
    smartwords = ['android','iphone','ipod','apple','htc','dell','samsung','lg','ipad','galaxy','sony','note','tab','tablet','phone','budget','nokia','linux','gadget','black','blackberry','belkin','smart','nexus','oneplus','watch','motorola','google','huawei','g3','g4','acer','xbox','mobile','lumia','web','gt-i9100','gt-i9200','gt-i9300','gt-i9100t','sm-g900f','sm-g900i','sm-g900','sm-g920','sm-g920i','sm-g920f','windows', 'sm-g900f']
    camerawords = ['canon','camera','nikon','webcam','cam','powershot']
    license = ['safenet']
    cdrom = ['cddvd', 'dvdram', 'cdram']

    for x,usb in usbs.iteritems():
        try:
            namelower = usb['name'].lower()
            html.write('\t\tName: '+usb['name'])
            for word in namelower.replace("_"," ").split(" "):
                related = 0
                if word in networds:
                    html.write(" | Related: Network")
                    related = 1
                    break
                elif word in storagewords:
                    html.write(" | Related: Disk-on-Key / External HardDrive")
                    related = 1
                    break
                elif word in smartwords:
                    html.write(" | Related: Smartphone / Media Device")
                    related = 1
                    break
                elif word in camerawords:
                    html.write(" | Related: Camera")
                    related = 1
                    break
                elif word in license:
                    html.write(" | Related: License device")
                    related = 1
                    break
                elif word in cdrom:
                    html.write(" | Related: External CD/DVD")
                    related = 1
                    break
            if related == 0:
                html.write(" | Related: N/A")
            html.write(' | Type: '+usb['type'])

            if usb['serial'] != "&nbsp;":
                html.write(' | Serial Number: '+usb['serial'])
            else:
                html.write(' | Serial Number: N/A')

            date = usb['ldate'].split("|")
            date = date[0] + " - " + date[1]
            html.write(' | Date: '+date+'\n')
            # To add the first date use: usb['fdate']
        except:
            pass


    # SoundTest ###############################
    ###########################################
    html.write('\nAudio (Sound and Record):\n')

    html.write("\tRecord:\n")
    if not recorded:
        html.write("\t\tMicrophone not found\n")
    else:
        html.write("\t\tSuccessfuly recorded, need human hear to check the record at "+tempdir+"\soundrecord.wav")

    html.write("\tSound:\n")
    if not played:
        html.write("\t\tSpeakers not found\n")
    else:
        html.write("\t\tSuccessfuly played sound, need human hear to check the sound at "+tempdir+"\soundplay.wav")
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    ########### END GENERAL ###################
    ###########################################


    ###########################################
    # END ############################### END #
    ###########################################

    html.close()
    print "Opens the text file..."
    os.system("start "+tempdir+"/panorama.txt")



def hibernate():
    os.system("powercfg.exe /h on")
    os.system("shutdown.exe /h")

class mainmenu():
    def __init__(self):
        self.master = Tk()
        self.master.title("Panorama")
        self.master.configure(bg='#072144')
        try:
            self.master.iconbitmap('sources\panorama.ico')
        except:
            pass

        logo = PhotoImage(file = r"sources\guimgs\logo.gif")
        label = Label(image = logo, borderwidth=0)
        label.image = logo
        label.grid(row = 1, column = 1, padx = 5, pady = 5)
        
        report = PhotoImage(file = r"sources\guimgs\report.gif")
        Button(self.master, image = report, borderwidth=0, bg='#072144', width=25, command=writehtml).grid(row=3, column=1, sticky=W+E,  pady=5, padx=5)

        text = PhotoImage(file = r"sources\guimgs\text.gif")
        Button(self.master, image = text, borderwidth=0, bg='#072144', width=25, command=writetextfile).grid(row=4, column=1, sticky=W+E,  pady=5, padx=5)

        hibernatei = PhotoImage(file = r"sources\guimgs\hibernate.gif")
        Button(self.master, image = hibernatei, borderwidth=0, bg='#072144',  command=hibernate).grid(row=5, column=1, sticky=W+E,  pady=5, padx=5)

        closendelete = PhotoImage(file = r"sources\guimgs\closendelete.gif")
        Button(self.master, image = closendelete, borderwidth=0, bg='#072144',  command=self.qandd).grid(row=6, column=1, sticky=W+E,  pady=5, padx=5)

        close = PhotoImage(file = r"sources\guimgs\close.gif")
        Button(self.master, image = close, borderwidth=0, bg='#072144', width=195, command=self.master.destroy).grid(row=7, column=1, sticky=N+E,  pady=5, padx=5)

        about = PhotoImage(file = r"sources\guimgs\about.gif")
        Button(self.master, image = about, borderwidth=0, bg='#072144', width=195, command=self.about).grid(row=7, column=1, sticky=S+W,  pady=5, padx=5)

        mainloop()

    def qandd(self):
        answer = tkMessageBox.askquestion("Delete", "Delete temp files and exit?", icon='warning')
        if answer.lower() == 'yes':
            print "Deleting 'panorama' temp files...\nEjecting disk...\nClosing app..."
            os.system("rmdir /s /q "+tempdir)
            self.master.destroy()
            ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)

    def about(self):
        tkMessageBox.showinfo("About", "PANORAMA\nVersion: v1.0\nSupports Windows 2000 and up.\n*Tested on up to Windows 8.1 64Bit\n\nGithub page: https://github.com/AlmCo/Panorama\nBy Almog Cohen, almogcn@gmail.com")

print "^",
recorded, played = fromhostget().soundtest()
print "^",
hostname = fromhostget().hostname
print "^ ^",
osver, ossp, osarch, fullos, osidate = fromhostget().os()
print "^ ^",
serialnumber = fromhostget().serialnumber()
print "^ ^",
firewall, firewallrules = fromhostget().firewall()
print "^",
hotfixs, hotfixCount = fromhostget().hotfixs()
print "^ ^",
mcafee = fromhostget().mcafee()
print "^ ^",
wireless = fromhostget().wireless()
print "^",
prefetch = fromhostget().prefetch()
print "^",
usbs,detectedWireless = fromhostget().usbdeview()
print "^ ^",
highusers,lowusers = fromhostget().usersinfo()
print "^",
installedsoftwares = fromhostget().softwares()
print "^ ^",
ips = fromhostget().ips()
print "^ ^",
macs = fromhostget().macs()
print "^ ^",
netstat = fromhostget().netstat()
print "^ ^",
startup = fromhostget().startup()
print "^ ^",
tasks = fromhostget().tasks()
print "^",
processes = fromhostget().processes()
print "^"
print "Opens main menu..."

mainmenu()