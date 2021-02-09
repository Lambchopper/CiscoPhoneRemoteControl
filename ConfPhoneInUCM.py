##################################################
# Remote Phone Control Configuration Tool
# Version 1.0
# 
# This tool is used to connect to UCM, collect a
# list of phone and end user accounts via AXL and
# allow the user to pick a phone and user to 
# configure for remote Phone Control.
#
# The script will use AXL to make the following
# changes:
# Enable the WebUI on the Phone
# Enable the SSH CLI on the Phone
# Configure the Phone's SSH UID and PWD
# Associate the end user with the Phone so that 
#   the Remote control tool can collect the Screen
#   shot from the phone
#
# By Dave Lamb - 11/19/2020
##################################################

from os.path import abspath
from urllib.parse import urljoin
from urllib.request import pathname2url
import re
import tkinter as tk
from tkinter import messagebox

import requests
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from lxml import etree
import time

# ===============================================
# Error Window Function Logins Window
# ===============================================

def ErrorWindow(strMessage):
    ErrorWindow = tk.Tk()
    ErrorWindow.title("Error!")
    MessageLBL = tk.Label(ErrorWindow, text=strMessage)

    def CloseProgEvnt(event):
        exit()
    
    def CloseProg():
        exit()
    
    OKBTN = tk.Button(ErrorWindow, width=9, text="Ok", command=CloseProg)

    MessageLBL.grid(row=0, column=0)
    OKBTN.grid(row=1, column=0)

    ErrorWindow.bind("<Return>", CloseProgEvnt)
    ErrorWindow.mainloop()


# ===============================================
# Configuration Window
# ===============================================
ConfigurationWindow = tk.Tk()
ConfigurationWindow.title("Configure Phone to Control")
Instructions = tk.Label(ConfigurationWindow, text="Remote Phone Control Configuration Tool\n\nEnter"\
    " UCM Creds and click connect.\nThen Choose the End User Account and Phone to configure.\n")

# Define Variables for Search functions in main window
FoundUserIndex = 0
UserFirstSearch = 0
FoundPhoneIndex = 0
PhoneFirstSearch = 0

def CloseProgEvnt(event):
    exit()
    
def CloseProg():
    exit()
    
def ExitConfigurationWin(event):
    ConfigurationWindow.destroy()

def RefreshUsersPhonesEvent(event):
    RefreshUsersPhones()
    
def RefreshUsersPhones():
    #Collect the values from the UCM fields
    global strUCMIP
    global strUCMAdmUserID
    global strUCMAdmPassword
    global UsersListBox
    global PhoneNameListBox
    global service
    global client
    global PhoneSSHUIDentry
    global PhoneSSHpwdentry

    #Collect Creds
    strUCMIP = UCMipentry.get()
    strUCMAdmUserID = UCMAdminUIDentry.get()
    strUCMAdmPassword = UCMAdminpwdentry.get()

    #Disable Creds
    UCMipentry['state'] = tk.DISABLED
    UCMAdminUIDentry['state'] = tk.DISABLED
    UCMAdminpwdentry['state'] = tk.DISABLED

    #Disable the Refresh Button
    RefreshBTN['state'] = tk.DISABLED

    #Collect path to the UCM AXL Schema
    #The schema files are downloaded from UCM > Applications > Plugins > Cisco AXL Toolkit
    wsdl = abspath('axlsqltoolkit/schema/11.5/AXLAPI.wsdl')
    location = 'https://{host}:8443/axl/'.format(host=strUCMIP)
    binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

    # Define http session and allow insecure connections
    session = Session()
    session.verify = False
    requests.packages.urllib3.disable_warnings()
    session.auth = HTTPBasicAuth(strUCMAdmUserID, strUCMAdmPassword)

    #Define a SOAP client
    transport = Transport(cache=SqliteCache(), session=session, timeout=20)
    client = Client(wsdl=wsdl, transport=transport)
    service = client.create_service(binding, location)

    #UCM AXL Call to retrieve Users
    try:
        userresponse = service.listUser(
            searchCriteria={
                'userid': '%'
            },
            returnedTags={
                'userid': True,
                'telephoneNumber': True
        })
        FailConnection = False
    except:
        ErrorWindow("UCM Connection Failed, Check Creds and IP and Try again")
        FailConnection = True
        RefreshBTN['state'] = tk.ACTIVE


    #UCM AXL Call to retrieve Users
    try:
        phoneresponse = service.listPhone(
            searchCriteria={
                'name': 'SEP%'
            },
            returnedTags={
                'name': True,
                'description': True,
                'model': True,
                'sshUserId': True
        })
        FailConnection = False
    except:
        ErrorWindow("UCM Connection Failed, Check Creds and IP and Try again")
        FailConnection = True
        RefreshBTN['state'] = tk.ACTIVE


    #If Successfully connected to UCM Populate ListBox
    if not FailConnection:
        #Collect the results of the AXL lookup
        UserList = userresponse['return'].user
        PhoneList = phoneresponse['return'].phone

        #Build the widgets for the Phone SSH Creds
        PhoneSSHUIDlabel = tk.Label(ConfigurationWindow, text="Phone SSH User:")
        PhoneSSHpwdlabel = tk.Label(ConfigurationWindow, text="Phone SSH Password:")
        PhoneSSHUIDentry = tk.Entry(ConfigurationWindow, width=30)
        PhoneSSHpwdentry = tk.Entry(ConfigurationWindow, show="*", width=30)

        #Build the widgets for the End User Selection Frame
        Userframe = tk.Frame(ConfigurationWindow)
        UserScollBar = tk.Scrollbar(Userframe)
        UsersListBox = tk.Listbox(Userframe, width=35, exportselection=0, yscrollcommand = UserScollBar.set)
        UserScollBar.config(command=UsersListBox.yview)
        UserSrchEntry = tk.Entry(Userframe)

        #Build the widgets for the Phone Selection Frame
        PhoneFrame = tk.Frame(ConfigurationWindow)
        PhoneScrollBar = tk.Scrollbar(PhoneFrame)
        PhoneNameListBox = tk.Listbox(PhoneFrame, exportselection=0, width=75, yscrollcommand = PhoneScrollBar.set)
        PhoneScrollBar.config(command=PhoneNameListBox.yview)
        PhoneSrchEntry = tk.Entry(PhoneFrame)
        PhoneHeaders = ["Model", "Name", "Description"]
        PhoneTableFormat = "{:<22}{:<37}{:<40}"

        #Define Function to search the Users List Box
        def SearchUsers():
            #Make variables globally available to track number of times we've seaarched the data
            global FoundUserIndex
            global UserFirstSearch
                       
            try:
                #Collect data from List Box
                UsersListBox.selection_clear(0, "end")
                FindUser = UserSrchEntry.get()
                AllUsers = UsersListBox.get(0, "end")
                NumOfUsers = UsersListBox.size()

                #Loop through the users in the list box
                for index,users in enumerate(AllUsers):
                    #Keep Track of which item in the list box we are checking
                    PassThroughLoop = index

                    #If the number of users found matches the list box item
                    #We're at the end of the search, prompt he user to start over and reset counters
                    if PassThroughLoop == NumOfUsers - 1:
                        #Select the last User, reset counters and notify user we found last match
                        UsersListBox.select_set(FoundUserIndex)
                        UsersListBox.activate(FoundUserIndex)
                        UsersListBox.see(FoundUserIndex)
                        FoundUserIndex = 0
                        PassThroughLoop = 0
                        UserFirstSearch = 0
                        #messagebox.showwarning(title="Reached End", message="We've reached the bottom of the 
                        # list.\n\nPlease click search to start again from top or modify your search string")
                        break
                    
                    #If we're not on the last item, check to see if list box item matches the string in the 
                    # Search Entry Field
                    if FindUser.lower() in users.lower(): 
                        if FoundUserIndex == 0 and UserFirstSearch == 0:
                            #If the FoundUserIndex is 0 and UserFirstSearch, then we found the first match
                            #Select and Activate that Item, collect index to count passes through the data 
                            # and set Counter tracking first pass to 1
                            UsersListBox.select_set(index)
                            UsersListBox.activate(index)
                            UsersListBox.see(index)
                            FoundUserIndex = index
                            UserFirstSearch = 1
                            break
                        elif index <= FoundUserIndex:
                            #If Index is less than or equal to Found User Index, then we've already found 
                            # this user, skip
                             pass
                        elif index > FoundUserIndex:
                            #If Index is Greater than Found User and less than total number of users, 
                            # this is a newly found user
                            #Select and Activate that Item, collect index to count passes through 
                            # the data and set Counter tracking first pass to 1
                            UsersListBox.selection_clear(FoundUserIndex)
                            UsersListBox.select_set(index)
                            UsersListBox.activate(index)
                            UsersListBox.see(index)
                            FoundUserIndex = index
                            break

                            
            except ValueError:
                messagebox.showwarning("Search", "User Not Found")
                
        #Define Function to search the Phones List Box
        def SearchPhones():
            #Make variables globally available to track number of times we've seaarched the data
            global FoundPhoneIndex
            global PhoneFirstSearch
                       
            try:
                #Collect data from List Box
                PhoneNameListBox.selection_clear(0, "end")
                FindPhone = PhoneSrchEntry.get()
                AllPhones = PhoneNameListBox.get(0, "end")
                NumOfPhones = PhoneNameListBox.size()

                #Loop through the users in the list box
                for index,phones in enumerate(AllPhones):
                    #Keep Track of which item in the list box we are checking
                    PassThroughLoop = index

                    #If the number of users found matches the list box item
                    #We're at the end of the search, prompt he user to start over and reset counters
                    if PassThroughLoop == NumOfPhones - 1:
                        #Select the last Phone, reset counters and notify user we found last match
                        PhoneNameListBox.select_set(FoundPhoneIndex)
                        PhoneNameListBox.activate(FoundPhoneIndex)
                        PhoneNameListBox.see(FoundPhoneIndex)
                        FoundPhoneIndex = 0
                        PassThroughLoop = 0
                        PhoneFirstSearch = 0
                        #messagebox.showwarning(title="Reached End", message="We've reached the bottom of 
                        # the list.\n\nPlease click search to start again from top or modify your search string")
                        break
                    
                    #If we're not on the last item, check to see if list box item matches the string in the 
                    # Search Entry Field
                    if FindPhone.lower() in phones.lower(): 
                        if FoundPhoneIndex == 0 and PhoneFirstSearch == 0:
                            #If the FoundPhoneIndex is 0 and PhoneFirstSearch, then we found the first match
                            #Select and Activate that Item, collect index to count passes through the data and 
                            # set Counter tracking first pass to 1
                            PhoneNameListBox.select_set(index)
                            PhoneNameListBox.activate(index)
                            PhoneNameListBox.see(index)
                            FoundPhoneIndex = index
                            PhoneFirstSearch = 1
                            break
                        elif index <= FoundPhoneIndex:
                            #If Index is less than or equal to Found Phone Index, then we've already found 
                            # this user, skip
                             pass
                        elif index > FoundPhoneIndex:
                            #If Index is Greater than Found Phone and less than total number of users, 
                            # this is a newly found user
                            #Select and Activate that Item, collect index to count passes through the data 
                            # and set Counter tracking first pass to 1
                            PhoneNameListBox.selection_clear(FoundPhoneIndex)
                            PhoneNameListBox.select_set(index)
                            PhoneNameListBox.activate(index)
                            PhoneNameListBox.see(index)
                            FoundPhoneIndex = index
                            break

                            
            except ValueError:
                messagebox.showwarning("Search", "Phone Not Found")
                
        UserSrchBTN = tk.Button(Userframe, width=9, text="Srch User", command=SearchUsers)
        PhoneSrchBTN = tk.Button(PhoneFrame, width=9, text="Srch Phone", command=SearchPhones)
    
        #Populate the User List box with the AXL Results
        for user in UserList:
            UsersListBox.insert(tk.END, user.userid)
        
        #Populate the Phone List Box with the Axl Results
        PhoneNameListBox.insert(0, PhoneTableFormat.format(*PhoneHeaders))

        PhoneTableFormat = "{:<20}{:<28}{:<40}"
        for phone in PhoneList:
            PopulateList = [phone.model, phone.name, phone.description]
            
            #This solution only supports 78XX and 88XX phones, so only populate those in to the list box
            RegEx = "Cisco [78]8\d\d"
            MatchRegEx = re.match(RegEx, PopulateList[0])

            if MatchRegEx:
                PhoneNameListBox.insert(tk.END, PhoneTableFormat.format(*PopulateList))

        #Put the Widgets into the frames
        PhoneSSHUIDlabel.grid(row=5, column=2, sticky='e')
        PhoneSSHUIDentry.grid(row=5, column=3, padx=5, sticky='w')
        PhoneSSHpwdlabel.grid(row=6, column=2, sticky='e')
        PhoneSSHpwdentry.grid(row=6, column=3, padx=5, sticky='w')

        UserSrchEntry.grid(row=0, column=0, sticky='w')
        UserSrchBTN.grid(row=0, column=0, sticky='e')
        UsersListBox.grid(row=1, column=0, sticky='e')
        UserScollBar.grid(row=1, column=1, sticky='nsw')
        Userframe.grid(row=7, column=0)

        PhoneSrchEntry.grid(row=0, column=0, sticky='w')
        PhoneSrchBTN.grid(row=0, column=0, sticky='e')
        PhoneNameListBox.grid(row=1, column=0, sticky='e')
        PhoneScrollBar.grid(row=1, column=1, sticky='nsw')
        PhoneFrame.grid(row=7, column=1, columnspan=3)

        #Enable the OK Button
        OKBTN['state'] = tk.NORMAL

def ConfigureRemoteControl():
    try:
        UCMEndUser = UsersListBox.get(UsersListBox.curselection())
    except:
        messagebox.showinfo(title="No End User", message="No end user is selected for association."\
            "\nPlease Try again.")
        return
    
    try:
        PhoneResult = PhoneNameListBox.get(PhoneNameListBox.curselection())
        PhoneToConfigureList = PhoneResult.split()
        PhoneToConfigure = PhoneToConfigureList[2]
    except:
        messagebox.showinfo(title="No Phone", message="No Phone is selected for association.\nPlease Try again.")
        return
    
    strPhoneSSHUserID = PhoneSSHUIDentry.get()
    strPhoneSSHPwd = PhoneSSHpwdentry.get()

    #Confirm we have everything to proceed or cancel and go back
    if not strPhoneSSHUserID:
        messagebox.showinfo(title="No SSH User", message="You have not entered an SSH User to configure."\
            "\nPlease Try again.")
        return
    if not strPhoneSSHPwd:
        messagebox.showinfo(title="No SSH Password", message="You have not entered an SSH Password to"\
            " configure.\nPlease Try again.")
        return
    if len(strPhoneSSHPwd) < 8:
        messagebox.showinfo(title="SSH Password too short", message="Your SSH Password must be greater"\
            " than 8 characters long.\nPlease Try again.")
        return

    # Create an associated devices object
    devices = {
            'device': []
        }
    devices[ 'device' ].append( PhoneToConfigure )

    # Execute the updateUser request using the devices object
    try:
	    resp = service.updateUser(
            userid = UCMEndUser,
            associatedDevices = devices,
            homeCluster = True,
            )
    except:
        ErrorWindow("UCM Update of user device association failed")
        return

    try:
        #Define the XML Elements that are needed for the vendorConfig (Device Specific Settings)
        webAccess = etree.Element( 'webAccess' )
        webAccess.text = '0'
        sshAccess = etree.Element( 'sshAccess' )
        sshAccess.text = '0'
    
        #Append them in to an array and define them as the Zeep XSD Type
        vendorConfig = []
        vendorConfig.append( webAccess )
        vendorConfig.append( sshAccess )
        xvcType = client.get_type( 'ns0:XVendorConfig' )

        #Execute the updatePhone Method and use the vendorConfig Array to update the phone
        resp = service.updatePhone(
            name = PhoneToConfigure,
            sshUserId = strPhoneSSHUserID,
            sshPwd = strPhoneSSHPwd,
            vendorConfig =  xvcType( vendorConfig )
            )

    except:
        ErrorWindow("UCM configuration of phone failed")
        return

    messagebox.showinfo(
        title="Remote Control Configured",
        message="The Phone: " + PhoneToConfigure + "\nand the User: " + UCMEndUser + "\nhave been"\
            " configured for Remote Control.\n\nIt may take up a minute or more for the Phone's"\
            " ssh service to start."
        )
    ConfigurationWindow.destroy()
    exit()

#Build the Widgets to login to UCM with Admin Creds to get AXL data
UCMiplabel = tk.Label(ConfigurationWindow, text="UCM IP or Hostname:")
UCMAdminUIDlabel = tk.Label(ConfigurationWindow, text="UCM Administrator User:")
UCMAdminpwdlabel = tk.Label(ConfigurationWindow, text="UCM Administrator Password:")
UCMipentry = tk.Entry(ConfigurationWindow, width=30)
UCMAdminUIDentry = tk.Entry(ConfigurationWindow, width=30)
UCMAdminpwdentry = tk.Entry(ConfigurationWindow, show="*", width=30)
UCMipentry.focus_force()

RefreshBTN = tk.Button(ConfigurationWindow, width=9, text="Connect", command=RefreshUsersPhones)
OKBTN = tk.Button(ConfigurationWindow, width=9, text="Ok", state="disabled", command=ConfigureRemoteControl)
CancelBTN = tk.Button(ConfigurationWindow, width=9, text="Cancel", command=CloseProg)

#load the Widgets to login to UCM with Admin Creds on to  the main window
Instructions.grid(row=0, column=0, rowspan=3, padx=7, columnspan=2)
UCMiplabel.grid(row=0, column=2, sticky='e')
UCMipentry.grid(row=0, column=3, padx=5, sticky='w')
UCMAdminUIDlabel.grid(row=1, column=2, sticky='e')
UCMAdminUIDentry.grid(row=1, column=3, padx=5, sticky='w')
UCMAdminpwdlabel.grid(row=2, column=2, sticky='e')
UCMAdminpwdentry.grid(row=2, column=3, padx=5, sticky='w')
RefreshBTN.grid(row=3, column=0, padx=5, sticky='w')
OKBTN.grid(row=3, column=3, padx=5, sticky='w')
CancelBTN.grid(row=3, column=3, padx=5, sticky='e')

#Define Events
ConfigurationWindow.bind("<Escape>", CloseProgEvnt)

#Center Window on screen
ConfigWindowWidth = ConfigurationWindow.winfo_reqwidth()
ConfigWindowHeight = ConfigurationWindow.winfo_reqheight()
PositionRight = int(ConfigurationWindow.winfo_screenwidth()/2.5 - ConfigWindowWidth/2)
PositionDown = int(ConfigurationWindow.winfo_screenheight()/3 - ConfigWindowHeight/2)
ConfigurationWindow.geometry("+{}+{}".format(PositionRight, PositionDown))

ConfigurationWindow.mainloop()