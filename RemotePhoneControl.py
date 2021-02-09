##################################################
# Remote Phone Control
# Version 1.1
# 
# Phone Remote Control is used to automate the
# the view of the phone screenshot feature
# and using an SSH Session to perform remote
# control functions
# Phone CLI Commands
#    "dial dn <num>" allows you to
#       remotely have a phone dial a number
#    "phone key <keyvalue>" allows you
#       to remotely press phone keys
#
# 7900 Series Phones are not suported, they do not
#     have the "phone key" command necessary
# 9900 Series Phones are not supported, they have
#     the commands in the CLI, but they do not function
#     Tested on 9971 with 9.4(2)SR4 code, the newest 
#     available at the time of testin - 8/27/2020
#
# Version 1.1
# Created for Converged Technology Group
# By Dave Lamb - 8/27/2020
#
# V1.1 Fixes:
# Bug where app won't close if SSH Session Times out
# Fixed an issue where the windows didn't have focus when started
# Made IP Address field have focus when Login screen started for easier data entry
# Added feature where app checks connectivity before sending key command to phone with option to reconnect
# Added feature where the app auto refreshes the screen every 1 second.
# Added feature where image is resized to 396px width to improve the GUI look (7841 is 396x162)
#     This essentially reduces the size of the 8865 and other images from their default
#     of 800x480 to 396x238.
##################################################

# ===============================================
# Import Required Python Modules
# ===============================================
# Backwards compatibility
#from __future__ import print_function, unicode_literals, division

import os
from sys import exit
import tkinter as tk
from tkinter import messagebox
import urllib.request
import paramiko
from paramiko_expect import SSHClientInteraction
from functools import partial
from PIL import Image, ImageTk
#print("Imported Modules successfully")

#Global Functions
def CloseProg():
    exit()

# ===============================================
# Welcome Window
# ===============================================
WelcomeWindow = tk.Tk()
WelcomeWindow.title("Welcome to Phone Control")
Instructions = tk.Label(WelcomeWindow, text="Remote Phone Control Tool\n\nBefore Continuing the Phone's WebUI and SSH service needs to be enabled.\nThe SSH User and Password meed to be set on the phone.\nYou'll also need a UCM end user account that is configured to control the phone\n")
WelcomeWindow.focus_force()

#Define Functions for Events
def CloseProgEvnt(event):
    CloseProg()
    
def ExitWelcomeWin(event):
    WelcomeWindow.destroy()

#Define Button widgets
OKBTN = tk.Button(WelcomeWindow, width=9, text="Ok", command=WelcomeWindow.destroy)
CancelBTN = tk.Button(WelcomeWindow, width=9, text="Cancel", command=CloseProg)

#Place Buttons
Instructions.grid(row=0, column=0)
OKBTN.grid(row=1, column=0, sticky='w')
CancelBTN.grid(row=1, column=0, sticky='e')

#Define Events
WelcomeWindow.bind("<Return>", ExitWelcomeWin)
WelcomeWindow.bind("<Escape>", CloseProgEvnt)

#Center Window on screen
WelcomeWindowWidth = WelcomeWindow.winfo_reqwidth()
WelcomeWindowHeight = WelcomeWindow.winfo_reqheight()
PositionRight = int(WelcomeWindow.winfo_screenwidth()/2.2 - WelcomeWindowWidth/2)
PositionDown = int(WelcomeWindow.winfo_screenheight()/2 - WelcomeWindowHeight/2)
WelcomeWindow.geometry("+{}+{}".format(PositionRight, PositionDown))

WelcomeWindow.mainloop()

# ===============================================
# Collect Logins Window
# ===============================================
LoginsWindow = tk.Tk()
LoginsWindow.title("Phone Connection Info")
LoginsWindow.focus_force()

#Define Functions
def CollectInfo():
    global strPhoneIP
    global strSSHUserID
    global strSSHPassword
    global strScreenShotUID
    global strScreenShotPWD

    strPhoneIP = phoneipentry.get()
    strSSHUserID = sshuidentry.get()
    strSSHPassword = sshpwdentry.get()
    strScreenShotUID = useruidentry.get()
    strScreenShotPWD = userpwdentry.get()
    LoginsWindow.destroy()

def CollectInfoEvent(event):
    CollectInfo()

#Define the button, label and entry Widgets
phoneiplabel = tk.Label(LoginsWindow, text="Phone IP Address")
sshuidlabel = tk.Label(LoginsWindow, text="SSH User")
sshpwdlabel = tk.Label(LoginsWindow, text="SSH Password")
useruidlabel = tk.Label(LoginsWindow, text="UCM User")
userpwdlabel = tk.Label(LoginsWindow, text="UCM Password")

phoneipentry = tk.Entry(LoginsWindow)
sshuidentry = tk.Entry(LoginsWindow)
sshpwdentry = tk.Entry(LoginsWindow, show="*")
useruidentry = tk.Entry(LoginsWindow)
userpwdentry = tk.Entry(LoginsWindow, show="*")
    
OKBTN = tk.Button(LoginsWindow, width=9, text="Ok", command=CollectInfo)
CancelBTN = tk.Button(LoginsWindow, width=9, text="Cancel", command=CloseProg)

#Place the Widgets
phoneiplabel.grid(row=0, column=0, sticky='e')
phoneipentry.grid(row=0, column=1, sticky='w')
sshuidlabel.grid(row=1, column=0, sticky='e')
sshuidentry.grid(row=1, column=1, sticky='w')
sshpwdlabel.grid(row=2, column=0, sticky='e')
sshpwdentry.grid(row=2, column=1, sticky='w')
useruidlabel.grid(row=3, column=0, sticky='e')
useruidentry.grid(row=3, column=1, sticky='w')
userpwdlabel.grid(row=4, column=0, sticky='e')
userpwdentry.grid(row=4, column=1, sticky='w')
phoneipentry.focus_force()

OKBTN.grid(row=5, column=0, sticky='w')
CancelBTN.grid(row=5, column=1, sticky='e')

#Define Events
LoginsWindow.bind("<Return>", CollectInfoEvent)

#Center Window on screen
LoginsWindowWidth = LoginsWindow.winfo_reqwidth()
LoginsWindowHeight = LoginsWindow.winfo_reqheight()
PositionRight = int(LoginsWindow.winfo_screenwidth()/2 - LoginsWindowWidth/2)
PositionDown = int(LoginsWindow.winfo_screenheight()/2 - LoginsWindowHeight/2)
LoginsWindow.geometry("+{}+{}".format(PositionRight, PositionDown))

LoginsWindow.mainloop()

# ===============================================
# Error Window Function Logins Window
# ===============================================

#Take a message text and display it in an error window
def ErrorWindow(strMessage):
    ErrorWindow = tk.Tk()
    ErrorWindow.title("Error!")
    ErrorWindow.focus_force()

    #Define subfunction
    def CloseProgEvnt(event):
        CloseProg()

    #Define widgets
    MessageLBL = tk.Label(ErrorWindow, text=strMessage)  
    OKBTN = tk.Button(ErrorWindow, width=9, text="Ok", command=CloseProg)

    #Place Widgets in Window
    MessageLBL.grid(row=0, column=0)
    OKBTN.grid(row=1, column=0)

    #Define Event
    ErrorWindow.bind("<Return>", CloseProgEvnt)

    #Center Window on screen
    ErrorWindowWidth = ErrorWindow.winfo_reqwidth()
    ErrorWindowHeight = ErrorWindow.winfo_reqheight()
    PositionRight = int(ErrorWindow.winfo_screenwidth()/2.2 - ErrorWindowWidth/2)
    PositionDown = int(ErrorWindow.winfo_screenheight()/2 - ErrorWindowHeight/2)
    ErrorWindow.geometry("+{}+{}".format(PositionRight, PositionDown))

    ErrorWindow.mainloop()

# ===============================================
# Open the Phone Screen Shot Connection
# and get first copy of the screen shot
# ===============================================
# This section should be part of the connectivity dialog to
# be developed

# create a password manager
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

# Add the username and password.
# If we knew the realm, we could use it instead of None.
top_level_url = "http://" + strPhoneIP
password_mgr.add_password(None, top_level_url, strScreenShotUID, strScreenShotPWD)

handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

# create "opener" (OpenerDirector instance)
opener = urllib.request.build_opener(handler)

# use the opener to fetch a URL
image_url = "http://" + strPhoneIP + "/CGI/Screenshot"

try:
    # Install the opener.
    opener.open(image_url)
except:
    strErrMessage = "CTG Phone Control\n\nA failure to connect to the screenshot of the phone has occured\n\nConfirm that the WebUI is enabled.\nConfirm the IP Address.\n"
    ErrorWindow(strErrMessage)
    
# Now all calls to urllib.request.urlopen use our opener.
urllib.request.install_opener(opener)

# Get the image and prep it
# image_byt = urllib.request.urlopen(image_url).read()
urllib.request.urlretrieve(image_url, "screenshot.bmp")

try:
    img = Image.open("screenshot.bmp")
except:
    strErrMessage = "CTG Phone Control\n\nA failure to connect to the screenshot of the phone has occured\n\nConfirm the Screenshot credentials.\nConfirm that the account can control the phone.\nConfirm that the account has UCM End User Rights.\n"
    ErrorWindow(strErrMessage)
    
#print("Opened Connection to ScreenShot Successfully")

# ===============================================
# Open the Phone SSH Connection
# ===============================================
# Establishing the SSH Connection will be part of the connect dialog
# that is still to be developed.
# wrap it in a function so that we can reestablish it if the phone times out later

def ConnectToSsh(UserID, Password):
    global objInteract
    global objSsh

    # Instantiate the SSH Object
    objSsh = paramiko.SSHClient()
    objSsh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Begin SSH Connection
    try:
        objSsh.connect(strPhoneIP, username=UserID, password=Password)
        strFail = "SSH Object Connected Successfully"
    except:
        objSsh.close()
        strFail = "CTG Phone Control\n\nFailed SSH Connection\n"
        ErrorWindow(strFail)

    # Nowthat the SSH session is started, send the secondary login to the Phone
    # to enter debug mode.
    # Use Expect because the UC CLI takes to long to start and commands
    # vary in duration of run time.  Expect ensures we enter the
    # command at the appropriate time.
    objInteract = SSHClientInteraction(objSsh, timeout=120, display=False)
    objInteract.expect('.*log.*', default_match_prefix='')
    objInteract.send('debug')
    objInteract.expect('.*Password.*')
    objInteract.send('debug')

    #print("Debug Login complete")

ConnectToSsh(strSSHUserID, strSSHPassword)

# ===============================================
# The Phone Control Screen
# ===============================================
# Create Tkinter window
MainWindow = tk.Tk()
MainWindow.title("Remote Phone Control")
MainWindow.focus_force()

# Resize Image to 396 Pixels wide to make the GUI a little nicer (match 7841 width)
pixelwidth = 396
widthpercent = (pixelwidth/float(img.size[0]))
horizontalsize = int((float(img.size[1])*float(widthpercent)))
img = img.resize((pixelwidth,horizontalsize), Image.ANTIALIAS)

# Create the Photo Tkinter Widget
# Open Image with Pillow
photo = ImageTk.PhotoImage(img)
Label_img = tk.Label(MainWindow, image=photo)
Label_img.grid(row=0, column=1, columnspan=5, rowspan=5)

#Used to collect a new copy of the screen shot from the physical phone
def RefreshScreen(event):
    # Get the image
    urllib.request.urlretrieve(image_url, "screenshot.bmp")
    refresh_img = Image.open("screenshot.bmp")

    # Resize Image to 396 Pixels wide to make the GUI a little nicer (match 7841 width)
    pixelwidth = 396
    widthpercent = (pixelwidth/float(refresh_img.size[0]))
    horizontalsize = int((float(refresh_img.size[1])*float(widthpercent)))
    refresh_img = refresh_img.resize((pixelwidth,horizontalsize), Image.ANTIALIAS)

    # Reload the image in to the GUI
    refresh_photo = ImageTk.PhotoImage(refresh_img)
    Label_img.configure(image=refresh_photo)
    Label_img.image = refresh_photo

#function used to refresh the window in case someone is interacting with the physical phone
def AutoRefresh():
    #Refersh the screen and restart the refresh timer
    #First timer event is started by a command near the mainloop method
    MainWindow.event_generate("<<Refresh>>")
    MainWindow.after(1000, AutoRefresh)

# Define Functions for Buttons to send command to Phone
def SendPhoneKey(strKeyValue):
    strKeyCommand = "phone key " + strKeyValue
    #If the command can't be sent to the Phone, Assume the SSH session timed out or was disrupted
    #Prompt user to reconnect or end program
    try:
        objInteract.send(strKeyCommand)
    except:
        if messagebox.askokcancel("SSH timeout", "SSH Timed Out\n\nClick Ok to reestablish connection to the phone\nClick Cancel to Exit Application\n"):
            try:
                ConnectToSsh(strSSHUserID, strSSHPassword)
            except:
                #If we still can't reconnect terminate application
                ErrorWindow("Still Unable to connect to Phone\nClosing Application")
            #If the reconnection was successful, attempt the command again
            objInteract.send(strKeyCommand)
        else:
            #If the user cancels, gracefully terminate application
            #Remove Tremp File
            if os.path.exists("screenshot.bmp"):
                os.remove("screenshot.bmp")
            
            #Remove SSH Session from Memory
            objSsh.close()
            #Close duh winder
            MainWindow.destroy()

    #After command is sent to phone, give the phone a 100ms to regenerate the screen shot
    #If the phone doesn't redraw the SS fast enough, the auto refresh will pick up the change.
    #Shortened from 500ms to improve application performance.
    MainWindow.after(100)
    MainWindow.event_generate("<<Refresh>>")

#Clean up Function for closing the main window
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #If the ssh Session is still open clean up SSH Session
        if objSsh.get_transport is not None:
            objSsh.close()
        
        #Remove the temp file
        if os.path.exists("screenshot.bmp"):
            os.remove("screenshot.bmp")
        
        #Close duh winder
        MainWindow.destroy()

# Create the phone button widgets
SoftKey1BTN = tk.Button(MainWindow, text="SoftKey1", width=9, command=partial(SendPhoneKey, "526"))
SoftKey2BTN = tk.Button(MainWindow, text="SoftKey2", width=9, command=partial(SendPhoneKey, "527"))
SoftKey3BTN = tk.Button(MainWindow, text="SoftKey3", width=9, command=partial(SendPhoneKey, "528"))
SoftKey4BTN = tk.Button(MainWindow, text="SoftKey4", width=9, command=partial(SendPhoneKey, "529"))
Line1BTN = tk.Button(MainWindow, text="Line1", width=8, command=partial(SendPhoneKey, "530"))
Line2BTN = tk.Button(MainWindow, text="Line2", width=8, command=partial(SendPhoneKey, "531"))
Line3BTN = tk.Button(MainWindow, text="Line3", width=8, command=partial(SendPhoneKey, "532"))
Line4BTN = tk.Button(MainWindow, text="Line4", width=8, command=partial(SendPhoneKey, "533"))
Line5BTN = tk.Button(MainWindow, text="Line5", width=8, command=partial(SendPhoneKey, "534"))
Line6BTN = tk.Button(MainWindow, text="Line6", width=8, command=partial(SendPhoneKey, "536"))
Line7BTN = tk.Button(MainWindow, text="Line7", width=8, command=partial(SendPhoneKey, "537"))
Line8BTN = tk.Button(MainWindow, text="Line8", width=8, command=partial(SendPhoneKey, "538"))
Line9BTN = tk.Button(MainWindow, text="Line9", width=8, command=partial(SendPhoneKey, "539"))
Line10BTN = tk.Button(MainWindow, text="Line10", width=8, command=partial(SendPhoneKey, "540"))
BackBTN = tk.Button(MainWindow, text="Back", width=9, command=partial(SendPhoneKey, "525"))
EndCallBTN = tk.Button(MainWindow, text="EndCall", width=9, command=partial(SendPhoneKey, "555"))
NavUpBTN = tk.Button(MainWindow, text="Up", width=6, command=partial(SendPhoneKey, "544"))
NavDwnBTN = tk.Button(MainWindow, text="Down", width=6, command=partial(SendPhoneKey, "546"))
NavRtBTN = tk.Button(MainWindow, text="Right", width=6, command=partial(SendPhoneKey, "548"))
NavLftBTN = tk.Button(MainWindow, text="Left", width=6, command=partial(SendPhoneKey, "547"))
SelectBTN = tk.Button(MainWindow, text="Select", width=6, command=partial(SendPhoneKey, "545"))
VMailBTN = tk.Button(MainWindow, text="VMail", width=9, command=partial(SendPhoneKey, "549"))
SettingsBTN = tk.Button(MainWindow, text="Settings", width=9, command=partial(SendPhoneKey, "551"))
DirBTN = tk.Button(MainWindow, text="Directory", width=9, command=partial(SendPhoneKey, "550"))
VolUpBTN = tk.Button(MainWindow, text="Volume +", width=9, command=partial(SendPhoneKey, "542"))
VolDnBTN = tk.Button(MainWindow, text="Volume -", width=9, command=partial(SendPhoneKey, "543"))
Key1BTN = tk.Button(MainWindow, text="1\n", width=6, command=partial(SendPhoneKey, "514"))
Key2BTN = tk.Button(MainWindow, text="2\nabc", width=6, command=partial(SendPhoneKey, "515"))
Key3BTN = tk.Button(MainWindow, text="3\ndef", width=6, command=partial(SendPhoneKey, "516"))
Key4BTN = tk.Button(MainWindow, text="4\nghi", width=6, command=partial(SendPhoneKey, "517"))
Key5BTN = tk.Button(MainWindow, text="5\njkl", width=6, command=partial(SendPhoneKey, "518"))
Key6BTN = tk.Button(MainWindow, text="6\nmno", width=6, command=partial(SendPhoneKey, "519"))
Key7BTN = tk.Button(MainWindow, text="7\npqrs", width=6, command=partial(SendPhoneKey, "520"))
Key8BTN = tk.Button(MainWindow, text="8\ntuv", width=6, command=partial(SendPhoneKey, "521"))
Key9BTN = tk.Button(MainWindow, text="9\nwxyz", width=6, command=partial(SendPhoneKey, "522"))
Key10BTN = tk.Button(MainWindow, text="*\n", width=6, command=partial(SendPhoneKey, "523"))
Key11BTN = tk.Button(MainWindow, text="0\n", width=6, command=partial(SendPhoneKey, "513"))
Key12BTN = tk.Button(MainWindow, text="#\n", width=6, command=partial(SendPhoneKey, "524"))
HoldBTN = tk.Button(MainWindow, text="Hold", width=9, command=partial(SendPhoneKey, "557"))
TransfBTN = tk.Button(MainWindow, text="Transfer", width=9, command=partial(SendPhoneKey, "558"))
ConfBTN = tk.Button(MainWindow, text="Confernce", width=9, command=partial(SendPhoneKey, "559"))
HeadSetBTN = tk.Button(MainWindow, text="Headset", width=9, command=partial(SendPhoneKey, "552"))
SpeakerBTN = tk.Button(MainWindow, text="Speaker", width=9, command=partial(SendPhoneKey, "553"))
MuteBTN = tk.Button(MainWindow, text="Mute", width=9, command=partial(SendPhoneKey, "554"))

#Add buttons to window
SoftKey1BTN.grid(row=6, column=1)
SoftKey2BTN.grid(row=6, column=2)
SoftKey3BTN.grid(row=6, column=4)
SoftKey4BTN.grid(row=6, column=5)
Line1BTN.grid(row=0, column=0)
Line2BTN.grid(row=1, column=0)
Line3BTN.grid(row=2, column=0)
Line4BTN.grid(row=3, column=0)
Line5BTN.grid(row=4, column=0)
Line6BTN.grid(row=0, column=6)
Line7BTN.grid(row=1, column=6)
Line8BTN.grid(row=2, column=6)
Line9BTN.grid(row=3, column=6)
Line10BTN.grid(row=4, column=6)
BackBTN.grid(row=8, column=1)
EndCallBTN.grid(row=8, column=5)
NavUpBTN.grid(row=7, column=3)
NavDwnBTN.grid(row=9, column=3)
NavRtBTN.grid(row=8, column=4, sticky='w')
NavLftBTN.grid(row=8, column=2, sticky='e')
SelectBTN.grid(row=8, column=3)

VMailBTN.grid(row=11, column=0, columnspan=2)
SettingsBTN.grid(row=12, column=0, sticky='e')
DirBTN.grid(row=12, column=1)
VolUpBTN.grid(row=13, column=1)
VolDnBTN.grid(row=13, column=0, sticky='e')
Key1BTN.grid(row=11, column=2, sticky='e')
Key2BTN.grid(row=11, column=3)
Key3BTN.grid(row=11, column=4, sticky='w')
Key4BTN.grid(row=12, column=2, sticky='e')
Key5BTN.grid(row=12, column=3)
Key6BTN.grid(row=12, column=4, sticky='w')
Key7BTN.grid(row=13, column=2, sticky='e')
Key8BTN.grid(row=13, column=3)
Key9BTN.grid(row=13, column=4, sticky='w')
Key10BTN.grid(row=14, column=2, sticky='e')
Key11BTN.grid(row=14, column=3)
Key12BTN.grid(row=14, column=4, sticky='w')
HoldBTN.grid(row=11, column=5, columnspan=2)
TransfBTN.grid(row=12, column=5)
ConfBTN.grid(row=12, column=6, sticky='w')
HeadSetBTN.grid(row=13, column=5)
SpeakerBTN.grid(row=13, column=6, sticky='w')
MuteBTN.grid(row=14, column=5, columnspan=2)

# Create a refresh event to call the refresh function from other locations in code
MainWindow.bind("<<Refresh>>", RefreshScreen)
MainWindow.bind("<space>", RefreshScreen)

#Call Close Function to clean up on exiting the window
MainWindow.protocol("WM_DELETE_WINDOW", on_closing)

#After 1 Second, Refresh the screen when window starts
MainWindow.after(1000, AutoRefresh)

#Center Window on screen
MainWindowWidth = MainWindow.winfo_reqwidth()
MainWindowHeight = MainWindow.winfo_reqheight()
PositionRight = int(MainWindow.winfo_screenwidth()/2.5 - MainWindowWidth/2)
PositionDown = int(MainWindow.winfo_screenheight()/3 - MainWindowHeight/2)
MainWindow.geometry("+{}+{}".format(PositionRight, PositionDown))

MainWindow.mainloop()