import subprocess
subprocess.run("source dist/sadns-app.exe & python dnsquery.py -d test.sqlite", shell=True)