[<img src="https://cloud.githubusercontent.com/assets/15038417/18474722/2f78cc4e-79cc-11e6-801e-b8efd70ba471.png" width="380" />](https://cloud.githubusercontent.com/assets/15038417/18474722/2f78cc4e-79cc-11e6-801e-b8efd70ba471.png)

### What is PANORAMA?
Panorama was made to generate a wide report about Windows systems, support and tested on Windows XP SP2 and up.

Provide a fast solution as giving an initial overview to the incident, Currently performing quite basic report.

The tool doesn't require admin permissions and yet can provide you a professional report on any Windows computer locally or throughout the network (Using without GUI).

New - 'Files Finder' - Map all media files, Currenlty available from GUI only. (doc, docx, ppt, pptx, PDF, gif, png, jpg, jped, wmv, mp4, avi)

Report structure
---------
#### System:
  1. Users - Password, Admin, Last logon, Last password update
  2. Startup commands - Command, Active
  3. Task scheduler - Name, Next run, Status
  4. Installed Softwares - List
  5. Recently used files - List
  4. Active processes - Name, ID, Communication


#### Security:
  1. McAfee - Version, Dat Date, Quarantine, Exclusions, Logs
  2. Firewall - Status, Allowed applications
  3. Microsoft hotfixes - Date, List of packages


#### Networking:
  1. Network cards - List
  2. IP Address - IP, Gateway, DHCP, Date, IPv6
  3. MAC Address - List
  4. Net view - List
  5. Netstat - Local, Target, ID, Process, Status
  6. ARP Table - IP, MAC, Type
  7. Hosts file - Domain, Target IP
  

#### USB:
  1. USB - Name, Type, Serial number, Date
  2. USB Deview - Link
  

Report output options:
---------
  1. HTML - Web page
  2. Text file
 
Quick USER guide:
---------
  1. Run 'Panorama.exe' from bin folder:
  
    2.1 Double-click OR from CMD without arguments - Opens the GUI
    
    2.2 Run from CMD - with argument '-c' - writes the results to TXT file (%temp%/panorama):
    
    ```Panorama.exe -c```
  
  3. Can run from CMD with argument '-h' to see the tiny help screen.
    
  4. NO admin permissions is required :)

Compile:
---------
The original Panorama file compiled by:

```c:\Python27\Scripts\pyinstaller.exe --onefile --window --icon=panorama.ico Panorama.py```

Screenshots:
---------
[<img src="https://cloud.githubusercontent.com/assets/15038417/21966272/4b64c304-db79-11e6-98e8-1f9504fcc5bc.png" width="200" height="200" />](https://cloud.githubusercontent.com/assets/15038417/21966272/4b64c304-db79-11e6-98e8-1f9504fcc5bc.png)

Web report view:

[<img src="https://cloud.githubusercontent.com/assets/15038417/21966282/669acc54-db79-11e6-9acb-afd86140327a.png" width="200" height="110" />](https://cloud.githubusercontent.com/assets/15038417/21966282/669acc54-db79-11e6-9acb-afd86140327a.png)

Text report view:

[<img src="https://cloud.githubusercontent.com/assets/15038417/21966287/6ba000ca-db79-11e6-87bb-a6ca17a639f0.png" width="200" height="110" />](https://cloud.githubusercontent.com/assets/15038417/21966287/6ba000ca-db79-11e6-87bb-a6ca17a639f0.png)
