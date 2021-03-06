from msilib.schema import tables
import dnsquery
from pickle import TRUE
from tkinter import Image
from xmlrpc.client import boolean
import PySimpleGUI as sg
import json
import requests
from datetime import date
import os as s
import ctypes, sys
import subprocess
from subprocess import check_output
import sys
import paramiko
from threading import Thread
import signal


#Global Variable
username, password, loginstate = '', '', boolean
data, response, access_token = {}, '', ''

hostname = '192.168.68.120' 
myuser   = 'safwan'
mySSHK   = r'C:\Users\CFONe\.ssh\id_rsa.pub'

status_adult, status_safesearch, status_socialmedia, status_gambling, status_malware = False, False, False, False, False
# End Global variable

# Global theme
my_theme = {'BACKGROUND': '#0E345E',
            'TEXT': 'white',
            'INPUT': 'white',
            'TEXT_INPUT': 'black',
            'SCROLL': '#c7e78b',
            'BUTTON': ('white', '#4998F2'),
            'PROGRESS': ('#01826B', '#D0D0D0'),
            'BORDER': 2,
            'SLIDER_DEPTH': 0,
            'PROGRESS_DEPTH': 0}


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

"""START Home aka Dashboard for SA DNS Main Dekstop application"""
def home():
    global access_token, status_adult, status_safesearch, status_socialmedia, status_gambling, status_malware, username
    sg.theme_add_new('MyTheme', my_theme)
    sg.theme('MyTheme') 
        
    DARK_HEADER_COLOR = '#0E345E'
    WHITE = '#FFFFFF'

    menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

    today = date.today()
    top_banner = [[sg.Text('SA DNS Dashboard'+ ' '*22, font='Any 20', background_color='#4998F2', text_color = WHITE),
               sg.Text(today.strftime("%B %d, %Y"), font='Any 20', background_color='#4998F2', text_color = WHITE)]]

    homedash = [
        [sg.Text('Enter domain to be blacklisted:')],
        [sg.Input(key='-bl-', size = (36,1) ,enable_events= False, do_not_clear= False),sg.Button('Ok', bind_return_key= True, key = '-blok-')]
    ]
    settingdash = [
        [sg.Text('Enter domain to be whitelisted:')],
        [sg.Input(key='-wl-', size = (36,1),enable_events= False,do_not_clear= False),sg.Button('Ok', bind_return_key= True,key = '-wlok-' )]
    ]

    cmd1 = "su"
    cmd2 = "systemctl stop named"
    cmd3 = "systemctl stop named"

    layout = [
        [sg.Menu(menu_def, tearoff=True, text_color = '#2EBCBC')],
        [sg.Column(top_banner, size=(700, 60), pad=(0,0), background_color='#4998F2')],
        [sg.Frame(layout=[
            [sg.Output(size=(45, 6), font=('Poppins 10'), pad = (10,10))]
            ],
            title='Output', relief=sg.RELIEF_SUNKEN),
            sg.Frame(layout= [
                [sg.Image(r'.\Images\shldoff.png', pad =(70,10), key = 'shld' )],
                [sg.Button(pad = ((68,0),(0,5)), image_filename = r'.\Images\off.png', key='-TOGGLE-GRAPHIC-', button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0)]
                ,#[sg.Button('Off', button_color= 'white on red',size=(3, 1),  key='-B-'),  sg.Button('Exit')]
                ],
                title= 'State', relief = sg.RELIEF_SUNKEN, pad = ((60,0),(0,0)))],
        [sg.Frame(layout=[
        [sg.Checkbox('Adult', key = '-adult-' , default=status_adult, enable_events = True),  sg.Checkbox('Gambling', key = '-gamba-', pad = ((85,0),(0,0)) , default=status_gambling, enable_events = True)],
        [sg.Checkbox('Social Media',key = '-socmed-', default=status_socialmedia, enable_events = True ),  sg.Checkbox('Security (Malware)',key = '-sec-' , default=status_malware, enable_events = True, pad = ((40,0),(0,0)))],
        [sg.Text('Enable SafeSearch:'),sg.Radio('Yes! ', "RADIO1", default=status_safesearch, key = '-sson-', enable_events = True ), sg.Radio('No!', "RADIO1",key = '-ssoff-', default=not(status_safesearch), enable_events = True)]
        ],
        title='Categories', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags'),
        sg.Frame(layout =[
            [sg.TabGroup([[sg.Tab('Blacklist', homedash,  key='-mykey-', title_color = 'white' ),
                         sg.Tab('Whitelist', settingdash,title_color = 'white')]],
                        
                       key='-group1-',title_color = 'white',tab_background_color = '#0E345E' ,selected_background_color = '#4998F2' , pad = ((10,10),(10,10)),
                        )]
        ],relief=sg.RELIEF_SUNKEN, title='')
        ],
        [
            sg.Button('Save Settings', key = '-sv-'), 
            sg.Button('Update Domain (History)', key = '-udh-'),
            sg.Button('Update/Create Domain data (Live)', key = '-ucddl-'),
            sg.Button('Upload Domain (Live)', key = '-udl-'),
        ]
    ]
           

    window = sg.Window('SA DNS', layout, enable_close_attempted_event=True, size=(700,400), icon='./Images/favicon.ico')
    down = graphic_off = True
    # Get profile config user
    jsonResponse = getProfileConfig(access_token)
    adult = jsonResponse[0]['id']
    safesearch = jsonResponse[1]['id']
    socialmedia = jsonResponse[2]['id']
    gambling = jsonResponse[3]['id']
    malware = jsonResponse[4]['id']
    dbuser = username + ".sqlite"
    csv_user = username + ".csv"
    
    while True:
        event, values = window.read()
        
        if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit?', icon='./Images/favicon.ico') == 'Yes':
            break
        elif event == '-TOGGLE-GRAPHIC-':   # if the graphical button that changes images
            graphic_off = not graphic_off
            window['-TOGGLE-GRAPHIC-'].update(image_filename= r'.\Images\off.png' if graphic_off else r'.\Images\on.png')
            if graphic_off == False:
                # Do something When SADNS Filter On
                print('SA DNS Filter is enabled!! ')
                window['shld'].update( filename = r'.\Images\shldon.png')
                window.refresh()
                """
                In production later use static dns server (eg:192.168.68.120) | For testing use 8.8.8.8 Google DNS 
                """
                # s.system('netsh interface ip set dns name="Wi-Fi" static 192.168.68.120')
                s.system('netsh interface ip set dns name="Ethernet" static 8.8.8.8')
                process = subprocess.Popen(["env/Scripts/python", "dnsquery.py", "-d", dbuser])

            else:
                # Do something When SADNS Filter Off
                print('SA DNS Filter is disbled!! ')
                window['shld'].update( filename = r'.\Images\shldoff.png')
                window.refresh()
                s.system('netsh interface ip set dnsservers name="Ethernet" source=dhcp')
                # process = subprocess.Popen(["./env/Scripts/python", "dnsquery.py", "-d", dbuser, "-e", csv_user])
                # process2 = subprocess.Popen(["./env/Scripts/python", "updateDomain.py", csv_user, access_token])
                # s.system('netsh interface ip set dnsservers name="Wi-Fi" source=dhcp')
                

        elif event == '-sv-':
            print('Your settings have been saved!')
            #print(values)
            #send ssh command to run script
            ssh_cmnd()
            sg.popup_auto_close("Your settings have been Saved!!", icon='./Images/favicon.ico')
        elif event == '-udh-': # Update Domain (History) aka browser history
            print('Update domain(history) to dashboard')
            process_udh = subprocess.Popen(["./env/Scripts/python", "updateDomainHistory.py", access_token])
        elif event == '-ucddl-': # Update/Create Domain Data (Live)
            print('Update or Create Domain data from live dns query')
            process_ucddl = subprocess.Popen(["./env/Scripts/python", "dnsquery.py", "-d", dbuser, "-e", csv_user])
        elif event == '-udl-': # Upload Domain (Live)
            print('Updating domain to dashboard...')
            process_udl = subprocess.Popen(["./env/Scripts/python", "updateDomain.py", csv_user, access_token])
        #send api to update settings and refresh dns server     
        #When button ok in blacklist is pressed
        elif event == '-blok-':
            print(values['-bl-']+' has been added to blacklist.')
            putBlacklist(access_token,values['-bl-'])
        #When button ok in whitelist is pressed
        elif event == '-wlok-':
            print(values['-wl-']+' has been added to whitelist.')
            putWhitelist(access_token,values['-wl-'])
        #When tick button  ( Category Adult)
        elif event == '-adult-':
            if values["-adult-"] == True:
                print('Enable selected category : Adult is set to On')
                status = "True"
                putProfileConfig(access_token, adult, status)
            else:
                print('Disable selected category : Adult is set to Off')
                status = "False"
                putProfileConfig(access_token, adult, status)
        #When tick button  ( Category Gambling)
        elif event == '-gamba-':
            if values["-gamba-"] == True:
                print('Enable selected category : Gambling is set to On')
                status = "True"
                putProfileConfig(access_token, gambling, status)
            else:
                print('Disable selected category : Gambling is set to Off')
                status = "False"
                putProfileConfig(access_token, gambling, status)
        #When tick button  ( Category SocMed)
        elif event == '-socmed-':
            if values["-socmed-"] == True:
                print('Enable selected category : Social Media is set to On')
                status = "True"
                putProfileConfig(access_token, socialmedia, status)
            else:
                print('Disable selected category : Social Media is set to Off')
                status = "False"
                putProfileConfig(access_token, socialmedia, status)
        #When tick button  ( Category Sec)
        elif event == '-sec-':
            if values["-sec-"] == True:
                print('Enable selected category : Malware is set to On')
                status = "True"
                putProfileConfig(access_token, malware, status)
            else:
                print('Disable selected category : Malware is set to Off')
                status = "False"
                putProfileConfig(access_token, malware, status)
        elif event == '-sson-':
                print(' Safesearch is set to On')
                status = "True"
                putProfileConfig(access_token, safesearch, status)
        elif event == '-ssoff-':
                print(' Safesearch is set to Off')
                status = "False"
                putProfileConfig(access_token, safesearch, status)
    
    # process = subprocess.Popen(["./env/Scripts/python", "dnsquery.py", "-d", dbuser, "-e", csv_user])
    # Close the window if user Click 'X'
    window.close()
"""ENDING Home aka Dashboard for SA DNS Main Dekstop application"""
  
"""START Loading animation when login into the application"""
def custom_meter_example(data):
    global  response
    # layout the form
    layout = [[sg.Text('Loggin you in...sit tight')],
              [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress', bar_color = ('#4998F2','#FFFFFF'))],
              [sg.Cancel()]]

    # create the form
    window = sg.Window('SA DNS', layout, icon='./Images/favicon.ico')
    progress_bar = window['progress']
    # loop that would normally do something useful
    
    for i in range(2000):
        # check to see if the cancel button was clicked and exit loop if clicked
        event, values = window.read(timeout=0)
        
        if i == 1000:
            response = requests.post(
                    'https://sadns.herokuapp.com/api/users/token/', data=data)
        
        if event == 'Cancel' or event == None:
            break
        # update bar with loop value +1 so that bar eventually reaches the maximum
        progress_bar.update_bar(i+100, 2000)
    # done with loop... need to destroy the window as it's still open
    
    window.close()
    return response
"""END Loading animation when login into the application"""

"""START Login"""
def login():
    global username, password, loginstate, data, response , access_token
    
    # Set login window theme
    sg.theme_add_new('MyTheme', my_theme)
    sg.theme('MyTheme') 
   
    layout = [
        [sg.Text("", justification='center', size=(100,1) )],
        [sg.Image(r'.\Images\saDNS.png', pad =(100,1) )],
        [sg.Text("WELCOME TO SA DNS APPLICATION", justification='center', size=(100,1) )],
        [sg.Text("", justification='center', size=(100,1) )],
        [sg.Text("Log In", justification='center', size=(100,1) )],
        [sg.Text("Username", justification='center', size=(100,1))],
        [sg.InputText(key='-usrnm-', justification='center', size=(100,1))],
        [sg.Text("Password", justification='center', size=(100,1))],
        [sg.InputText(key='-pwd-', password_char='*', justification='center', size=(100,1))],
        [sg.Button('Ok', bind_return_key= True),sg.Button('Cancel')]
    ]

    window = sg.Window("SA DNS", layout,size=(300, 400), icon='./Images/favicon.ico')

    while True:
        event,values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        elif  values['-usrnm-'] == "" or values['-pwd-'] == "":
             sg.popup('Required Fields', 'Username/password should not be empty', text_color = "#FF4242", icon='./Images/favicon.ico')
        else:
            data = {
                "username": values['-usrnm-'],
                "password": values['-pwd-']
            }
            username = values['-usrnm-']
            try:
                custom_meter_example(data)                
                response_dict = json.loads(response.text)
                access_token = response_dict['access']
                sg.popup_auto_close("Welcome!", icon='./Images/favicon.ico')
                loginstate = TRUE
                break
            except Exception as e:
                sg.popup("Invalid Login!","Unable to log in with provided credentials.", 
                            title = "Invalid Login!", no_titlebar = False, 
                            icon = "red-error", line_width= 40, text_color = "#FF4242" )
    window.close()
"""END Login"""
 

"""START API Function"""
# Get the all Profile Config
def getProfileConfig(access_token):
  url = "https://sadns.herokuapp.com/api/profileConfig/"
  token = "Bearer " + str(access_token)
  print(token)
  headers = {
    "Authorization": token
  }
  response = requests.request("GET", url, headers=headers)
  jsonResponse = response.json()
  return jsonResponse

# Adjust certain profile config
def putProfileConfig(access_token, id, status):
    id = id #UUID
    status = status #string
    url = "https://sadns.herokuapp.com/api/profileConfig/" + id

    payload = {
        "cat_status" : status
    }
    token = "Bearer " + str(access_token)
    headers = {
        "Authorization": token
    }
    response = requests.request("PUT", url, headers=headers, data=payload)

def putBlacklist(access_token, domainbl):
    domainbl = domainbl #string
    url = "https://sadns.herokuapp.com/api/blacklist/"

    payload = {
        "bl_domain" : domainbl,
        "bl_comment": ''
    }
    token = "Bearer " + str(access_token)
    headers = {
        "Authorization": token
    }
    response = requests.request("POST", url, headers=headers, data=payload)

def putWhitelist(access_token, domainwl):
    domainwl = domainwl #string
    url = "https://sadns.herokuapp.com/api/whitelist/"

    payload = {
        "wl_domain" : domainwl,
        "wl_comment": ''
    }
    token = "Bearer " + str(access_token)
    headers = {
        "Authorization": token
    }
    response = requests.request("POST", url, headers=headers, data=payload)
"""END API Function"""

"""START Essential Function"""
def ssh_cmnd():
    ssh   = paramiko.SSHClient()  # will create the object
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # no known_hosts error
    ssh.connect(hostname, username=myuser, key_filename=mySSHK) 

    stdin, stdout, stderr = ssh.exec_command("sudo -S  -p '' python3 /home/safwan/Documents/FYP/user.py")
    stdin.write("Opcar123\n")
    stdin.flush()
    ssh.close()
"""END Essential Function"""

"""Start main application"""
def main():
    global status_adult, status_safesearch, status_socialmedia, status_gambling, status_malware
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'CompanyName.ProductName.SubProduct.VersionInformation') # Arbitrary string`
    
    is_admin()
    if is_admin():
        login()

        if loginstate == TRUE:
            # Set Profile Config Status by default
            jsonResponse = getProfileConfig(access_token)
            status_adult = jsonResponse[0]['cat_status']
            status_safesearch = jsonResponse[1]['cat_status']
            status_socialmedia = jsonResponse[2]['cat_status']
            status_gambling = jsonResponse[3]['cat_status']
            status_malware = jsonResponse[4]['cat_status']
            home()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

if __name__ == "__main__":
    main()