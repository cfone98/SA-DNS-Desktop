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
import sys

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

# This bit gets the taskbar icon working properly in Windows
if sys.platform.startswith('win'):
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'CompanyName.ProductName.SubProduct.VersionInformation') # Arbitrary string

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def home():

    sg.theme_add_new('MyTheme', my_theme)
    sg.theme('MyTheme') 
    # sg.theme_element_text_color ('#2EBCBC') 
    # sg.theme_text_color('#FFFFFF')
    # sg.theme_button_color(['White','#4998F2'])
    
    DARK_HEADER_COLOR = '#0E345E'
    WHITE = '#FFFFFF'

    menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

    today = date.today()
    top_banner = [[sg.Text('SA DNS Dashboard'+ ' '*24, font='Any 20', background_color=DARK_HEADER_COLOR, text_color = WHITE),
               sg.Text(today.strftime("%B %d, %Y"), font='Any 20', background_color=DARK_HEADER_COLOR, text_color = WHITE)]]

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
        #[sg.Menu(menu_def, tearoff=True, text_color = '#2EBCBC')],
        [sg.Column(top_banner, size=(700, 60), pad=(0,0), background_color=DARK_HEADER_COLOR)],
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
        [sg.Checkbox('Adult', key = '-cat1-' , enable_events = True),  sg.Checkbox('Gambling', pad = ((85,0),(0,0)))],
        [sg.Checkbox('Social Media'),  sg.Checkbox('Security', pad = ((40,0),(0,0)))],
        [sg.Text('Enable SafeSearch:'),sg.Radio('Yes! ', "RADIO1", default=True, ), sg.Radio('No!', "RADIO1")]
        ],
        title='Categories', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags'),
        sg.Frame(layout =[
            [sg.TabGroup([[sg.Tab('Blacklist', homedash,  key='-mykey-', title_color = '#2EBCBC' ),
                         sg.Tab('Whitelist', settingdash,title_color = '#2EBCBC')]],
                        
                       key='-group1-',title_color = '#2EBCBC', pad = ((10,10),(10,10)),
                        )]
        ],relief=sg.RELIEF_SUNKEN, title='')
        ],
            [sg.Button('Save Settings', key = '-sv-')]
    ]
           

    

    window = sg.Window('SA DNS', layout, enable_close_attempted_event=True, size=(700,400), icon='./Images/favicon.ico')
    down = graphic_off = True
    while True:
        event, values = window.read()
        
        if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit?', icon='./Images/favicon.ico') == 'Yes':
            break
        elif event == '-TOGGLE-GRAPHIC-':   # if the graphical button that changes images
            graphic_off = not graphic_off
            window['-TOGGLE-GRAPHIC-'].update(image_filename= r'.\Images\off.png' if graphic_off else r'.\Images\on.png')
            if graphic_off == False:
                print('SA DNS Filter is enabled!! ')
                window['shld'].update( filename = r'.\Images\shldon.png')
                window.refresh()
                s.system('netsh interface ip set dns name="Ethernet" static 185.37.37.37')
                
            else:
                print('SA DNS Filter is disbled!! ')
                window['shld'].update( filename = r'.\Images\shldoff.png')
                window.refresh()
                s.system('netsh interface ip set dnsservers name="Ethernet" source=dhcp')
                

        elif event == '-sv-':
            print('Your settings have been saved!')
            print(values)
            #send api to update settings and refresh dns server
            subprocess.Popen("ssh {user}@{host} {cmd}".format(user="safwan", host="192.168.68.120", cmd='mkdir test'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        elif event == '-blok-':
            print(values['-bl-']+' has been added to blacklist.')
        elif event == '-wlok-':
            print(values['-wl-']+' has been added to blacklist.')
        elif event == '-cat1':
            print('adult on')
            
            
    window.close()
  

def custom_meter_example(data):
    global  response
    # layout the form
    layout = [[sg.Text('Loggin you in...sit tight')],
              [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress',bar_color='#2EBCBC')],
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


username = ''
password = ''
loginstate = boolean

data = {}
response = ''


def login():
    global username,password,loginstate,data,response
    sg.theme_add_new('MyTheme', my_theme)
    sg.theme('MyTheme') 
    # sg.theme_element_text_color ('#2EBCBC') 
    # sg.theme_text_color('#0b112b')
    # sg.theme_button_color(['White','#4998F2'])
    layout = [
            [sg.Text("", justification='center', size=(100,1) )],
            [sg.Image(r'.\Images\saDNS.png', pad =(150,1) )],
            [sg.Text("WELCOME TO SA DNS APPLICATION", justification='center', size=(100,1) )],
            [sg.Text("", justification='center', size=(100,1) )],
            [sg.Text("Log In", justification='center', size=(100,1) )],
            [sg.Text("Username", justification='center', size=(100,1))],
            [sg.InputText(key='-usrnm-', justification='center', size=(100,1))],
            [sg.Text("Password", justification='center', size=(100,1))],
            [sg.InputText(key='-pwd-', password_char='*', justification='center', size=(100,1))],
            [sg.Button('Ok', bind_return_key= True),sg.Button('Cancel')]
            ]

    window = sg.Window("SA DNS", layout,size=(400, 400), icon='./Images/favicon.ico')

    while True:
        event,values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        elif  values['-usrnm-'] == "" or values['-pwd-'] == "":
             sg.popup(
            'Required Fields', 'Username/password should not be empty', text_color = "#FF4242", icon='./Images/favicon.ico')
        else:
            data = {
            "username": values['-usrnm-'],
            "password": values['-pwd-']
        }
            try:
                custom_meter_example(data)
                #response = requests.post(
                    #'http://localhost:8000/api-token-auth/', data=data)
                #custom_meter_example()
                print(response)
                #if response = 
                response_dict = json.loads(response.text)
                print(response_dict)
                token_out = response_dict['access']
                print(token_out)
                sg.popup_auto_close("Welcome!", icon='./Images/favicon.ico')
                loginstate = TRUE
                break
            except Exception as e:
                sg.popup("Invalid Login!","Unable to log in with provided credentials.", 
                            title = "Invalid Login!", no_titlebar = False, 
                            icon = "red-error", line_width= 40, text_color = "#FF4242" )
    window.close()

 
#'''
is_admin()
if is_admin():
    login()
    if loginstate == TRUE:
        home()

else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
#'''
#login()
#home()

'''
if __name__ == '__main__':
    home()

    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
'''  
'''
python .\manage.py runserver

'''