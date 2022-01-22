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

#sg.theme_previewer()



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False





def home():

    sg.theme('DarkBlue9') 
    sg.theme_element_text_color ('#2EBCBC') 
    sg.theme_text_color('#FFFFFF')
    sg.theme_button_color(['Black','#2EBCBC'])
    
    print(sg.theme_background_color(),
    sg.theme_border_width(),
    sg.theme_button_color(),
    sg.theme_element_background_color(),
    sg.theme_element_text_color(),
    sg.theme_input_background_color(),
    sg.theme_input_text_color(),
    sg.theme_progress_bar_border_width(),
    sg.theme_progress_bar_color(),
    sg.theme_slider_border_width(),
    sg.theme_slider_color(),
    sg.theme_text_color())
    DARK_HEADER_COLOR = '#1B2838'

    menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

    today = date.today()
    top_banner = [[sg.Text('SA DNS Dashboard'+ ' '*24, font='Any 20', background_color=DARK_HEADER_COLOR, text_color =  '#2EBCBC'),
               sg.Text(today.strftime("%B %d, %Y"), font='Any 20', background_color=DARK_HEADER_COLOR, text_color =  '#2EBCBC')]]

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
            [sg.Output(size=(45, 6), font=('Helvetica 10'), pad = (10,10))]
            ],
            title='Output', relief=sg.RELIEF_SUNKEN),
            sg.Frame(layout= [
                [sg.Image(r'C:\Users\CFONe\Pictures\shldoff.png', pad =(70,10), key = 'shld' )],
                [sg.Button(pad = ((68,0),(0,5)), image_filename = r'C:\Users\CFONe\Documents\STUDY\SEM 7\FYP\Ui\icons\off.png', key='-TOGGLE-GRAPHIC-', button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0)]
                ,#[sg.Button('Off', button_color= 'white on red',size=(3, 1),  key='-B-'),  sg.Button('Exit')]
                ],
                title= 'State', relief = sg.RELIEF_SUNKEN, pad = ((60,0),(0,0)))],
        [sg.Frame(layout=[
        [sg.Checkbox('Adult Content/Pornography', key = '-cat1-' , enable_events = True),  sg.Checkbox('Gambling')],
        [sg.Checkbox('Social Media' ),  sg.Checkbox('Fake News',pad = ((85,0),(0,0)))],
        [sg.Checkbox('Torrent/File-sharing' ),  sg.Checkbox('Malware', pad = (50,0))],
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
           

    

    window = sg.Window('SA DNS', layout, enable_close_attempted_event=True, size=(700, 400))
    down = graphic_off = True
    while True:
        event, values = window.read()
        
        if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit?') == 'Yes':
            break
        elif event == '-TOGGLE-GRAPHIC-':   # if the graphical button that changes images
            graphic_off = not graphic_off
            window['-TOGGLE-GRAPHIC-'].update(image_filename= r'C:\Users\CFONe\Documents\STUDY\SEM 7\FYP\Ui\icons\off.png' if graphic_off else r'C:\Users\CFONe\Documents\STUDY\SEM 7\FYP\Ui\icons\on.png')
            if graphic_off == False:
                print('SA DNS Filter is enabled!! ')
                window['shld'].update( filename = r'C:\Users\CFONe\Pictures\shldon.png')
                window.refresh()
                s.system('netsh interface ip set dns name="Ethernet" static 185.37.37.37')
                
            else:
                print('SA DNS Filter is disbled!! ')
                window['shld'].update( filename = r'C:\Users\CFONe\Pictures\shldoff.png')
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

    # create the form`
    window = sg.Window('Custom Progress Meter', layout)
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
    sg.theme('DarkBlue9') 
    sg.theme_element_text_color ('#2EBCBC') 
    sg.theme_text_color('#2EBCBC')
    sg.theme_button_color(['Black','#2EBCBC'])
    layout = [
            [sg.Image(r'C:\Users\CFONe\Pictures\shield3.png', pad =(70,10) )],
            [sg.Text("Log In")],
            [sg.Text("Username")],
            [sg.InputText(key='-usrnm-')],
            [sg.Text("Password")],
            [sg.InputText(key='-pwd-', password_char='*')],
            [sg.Button('Ok', bind_return_key= True),sg.Button('Cancel')]
            ]

    window = sg.Window("SA DNS", layout,size=(250, 300))

    while True:
        event,values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        elif  values['-usrnm-'] == "" or values['-pwd-'] == "":
             sg.popup(
            'Required Fields', 'Username/password should not be empty', text_color = "#FF4242")
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
                sg.popup_auto_close("Welcome!")
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