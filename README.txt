Phone Control - Used to remote control Phone
Created by. D.Lamb

This tool has two components. A configurator, which will allow you to search for a phone
and user in Cisco Call Manager and configure the phone with the WebUI Wnabled, SSH CLI Enabled,
a SSH UID and PWD.  It then add the selected phone as a controlled device to an End User 
account. These are required for the Remote control tool to work.

The second tool allows the user to remote connect to a phone and control it.  The tool
supports Cisco 7800 and 8800 Phones.  The tool will use the Phone's Screenshot to allow
remote viewing of the phone screen and will use the Phone's SSH CLI to issue button presses
remotely.

Note that this tool is intended for troubleshooting, some functionality, like typing Alpha
characters using the keypad don't function, due to the delayed timing of the phone's CLI.
The tool can be used to remote view the screen, so a local user can handle this function.

Required Python Libraries for Phone Control:
Tkinter  - GUI
urllib3  - Used to collect the Phone's screenshots
paramiko - Used to automate the SSH session with the Phone
ImageTk  - Used with the GUI to display the Phone's Screenshots

Notes about code in comments in PhoneControl.py

ConfPhoneInUCM - Used to configure UCM to control Phone

Required Python Libraries for onfiguring Phone Comntrol Script:
Tkinter  - GUI
zeep     - SOAP Client used to interact with Cisco UCM's AXL API
lxml     - Used to build the XML required to configure the Phone's Product Specific settings.
