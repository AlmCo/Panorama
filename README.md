[<img src="https://cloud.githubusercontent.com/assets/15038417/18474722/2f78cc4e-79cc-11e6-801e-b8efd70ba471.png" width="380" />](https://cloud.githubusercontent.com/assets/15038417/18474722/2f78cc4e-79cc-11e6-801e-b8efd70ba471.png)

### What is PANORAMA?
Panorama was made to generate a width report about Windows systems, support and tested on Windows 2000 and up.
Provide a fast solution as giving an initial overview to the incident, Currently performing quite basic report:

Report structure
---------
#### Software:
  1. Startup commands - The applications that start every startup
  2. Task scheduler - Shdeduler application with date
  3. Prefetch - Parsing all prefetch files to one table (Name, Date, Size, Path, Counter and last run time)
  4. Process list - The simple "tasklist /svn" with description
  5. Installed Softwares - List of all installed softwares

#### Security:
  1. Firewall allowed applications - List of all firewall rules
  2. McAfee - Version and setting, list of exclusions and intersting logs
  3. Microsoft updates and hotfixes

#### Networking:
  1. IP and MAC Address - List of address with dates
  2. Netstat - The simple "netstat -no" command
  3. Wireless cards - Connected wireless cards

#### General:
  1. Users - Sorted by administrator and regular users
  2. USB Connections - History of all usb connections with dates and serial number
  3. Speakers and microphone - Durability test

Report output options:
---------
  1. HTML - Opens with browser
  2. Text file - Opens with notepad
 
Quick USER guide:
---------
  1. Clone the Panorama by:
    ```git clone https://github.com/AlmCo/Panorama.git```
  2. Run bin/Panorama.exe
  3. Admin permissions is required only for prefetch.
  4. **Burn the 'bin' folder contents on read-only CD is recommanded.**

Developer guide:
---------
  * Under the 'src' folder has two files: Panorama.py and setup.py
  * Can be compiled by: ```python setup.py py2exe```
  * Reqierd dependencies (can be install by 'pip install'):
    *  Tkinter
    *  _winreg
    *  pyaudio
    *  wave
  * Reqierd files and folder:
    * Copy the folder 'sources' that under 'bin' folder
    * Copy all of the DLL and manifest files

Screenshots:
---------
[<img src="https://cloud.githubusercontent.com/assets/15038417/18474718/2d10cf38-79cc-11e6-921d-3364685b44ee.png" width="200" height="200" />](https://cloud.githubusercontent.com/assets/15038417/18474718/2d10cf38-79cc-11e6-921d-3364685b44ee.png)

Web report view:

[<img src="https://cloud.githubusercontent.com/assets/15038417/18474444/ab1abc1a-79ca-11e6-8d1b-cf6c2f7c867e.png" width="200" height="110" />](https://cloud.githubusercontent.com/assets/15038417/18474444/ab1abc1a-79ca-11e6-8d1b-cf6c2f7c867e.png)

Text report view:

[<img src="https://cloud.githubusercontent.com/assets/15038417/18503158/09b963c2-7a64-11e6-8fa9-9ee200e1f013.png" width="200" height="110" />](https://cloud.githubusercontent.com/assets/15038417/18503158/09b963c2-7a64-11e6-8fa9-9ee200e1f013.png)
