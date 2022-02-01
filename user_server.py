from pickle import TRUE
import requests
import json
import urllib
import subprocess

zoneHeader = """$TTL 5S
@       IN SOA sa.dnsfilter.com. root.dnsfilter.com. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        10S )   ; minimum
@       IN      NS      sa.dnsfilter.com.
@       IN      A       44.194.94.84\n\n"""

data = {
    "username": "user2022",
    "password": "abubaba1234"
}

api_url_profile = "https://sadns.herokuapp.com/api/profileConfig/"
api_url_auth = "https://sadns.herokuapp.com/api/users/token/"
api_url_bl = "https://sadns.herokuapp.com/api/blacklist/"
api_url_wl = "https://sadns.herokuapp.com/api/whitelist/"

state_adult = False
state_ss = False
state_gamba = False
state_socmed = False
state_malware = False

commentchar = "#"


response = requests.post(api_url_auth,data)
print(response)
response_dict = json.loads(response.text)
access_token = response_dict['access']
print(access_token)

#get profile settings
token = "Bearer " + str(access_token)
headers = {
    "Authorization": token
}
response2 = requests.request("GET",api_url_profile,headers = headers)
profileresp = response2.json()
print(response2)
state_adult = profileresp[0]['cat_status']
print(state_adult)
state_ss = profileresp[1]['cat_status']
state_socmed = profileresp[2]['cat_status']
state_gamba = profileresp[3]['cat_status']
state_malware = profileresp[4]['cat_status']

#get blacklist and whitelist
response3 = requests.request("GET",api_url_bl,headers = headers)
blresponse = response3.json()

for x in blresponse:
    print(x['bl_domain'])
    


#write to rpz file
f = open('/var/named/rpz.db', 'w')
f.write(zoneHeader)

blocklistporn = "https://raw.githubusercontent.com/mhhakim/pihole-blocklist/master/porn.txt"
blocklistsocmed = "https://media.githubusercontent.com/media/froxity/scriptSADNS/backup/socialmedia.txt"
blocklistmalware = ""
blocklistgamba = ""

safesearch = """; force Google SafeSerach
google.com                IN CNAME forcesafesearch.google.com.
www.google.com            IN CNAME forcesafesearch.google.com.
google.fr                 IN CNAME forcesafesearch.google.com.
www.google.fr             IN CNAME forcesafesearch.google.com.
; force youtube safe search
www.youtube.com           IN CNAME restrict.youtube.com.
m.youtube.com             IN CNAME restrict.youtube.com.
youtubei.googleapis.com   IN CNAME restrict.youtube.com.
youtube.googleapis.com    IN CNAME restrict.youtube.com.
www.youtube-nocookie.com  IN CNAME restrict.youtube.com.
; force bing strict
www.bing.com              IN CNAME strict.bing.com.
; force duckduckgo safe search
duckduckgo.com            IN CNAME safe.duckduckgo.com."""

if state_ss == True:    
    f.write(safesearch)
    f.write("\n")
                
if state_adult == True:    
    with urllib.request.urlopen(blocklistporn) as b:
        for bytes in b:

                line = bytes.decode("utf-8").strip()

                if (not line or line.startswith(commentchar)):
                        continue

                domain = line
                f.write(domain+"\tIN\tCNAME\t@\n")

if state_socmed == True:
    with urllib.request.urlopen(blocklistsocmed) as b:
        for bytes in b:

                line = bytes.decode("utf-8").strip()

                if (not line or line.startswith(commentchar)):
                        continue

                domain = line
                f.write(domain+"\tIN\tCNAME\t@\n")

if state_gamba == True:
    with urllib.request.urlopen(blocklistgamba) as b:
        for bytes in b:

                line = bytes.decode("utf-8").strip()

                if (not line or line.startswith(commentchar)):
                        continue

                domain = line
                f.write(domain+"\tIN\tCNAME\t@\n")

if state_malware == True:
    with urllib.request.urlopen(blocklistmalware) as b:
        for bytes in b:

                line = bytes.decode("utf-8").strip()

                if (not line or line.startswith(commentchar)):
                        continue

                domain = line
                f.write(domain+"\tIN\tCNAME\t@\n")


#add blocklist url
for x in blresponse:
    f.write(x['bl_domain']+"\tIN\tCNAME\t@\n")

f.close()
#remove whitelist domains
with open ('/var/named/rpz.db', 'r') as r:
    print(r.readlines())

#restart bind server
bashcommand = ["systemctl restart named"]
process = subprocess.Popen(bashcommand, stdout = subprocess.PIPE, shell = TRUE)
output,error = process.communicate()

print(output)
