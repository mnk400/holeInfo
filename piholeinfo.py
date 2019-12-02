import json
import time
import os
from urllib.request import urlopen
from colorama import Fore

url = "http://pi.hole/admin"

status_check = "%s/api.php?status" % url

summary_today = "%s/api.php?summary" % url


def nativejson(data):
    return json.loads(data)


def request(input_url, method='GET'):
    response = urlopen(input_url)
    return nativejson(response.read())


def check_status():
    response = request(status_check)
    return response['status']


def get_summary():
    response = request(summary_today)
    print(Fore.CYAN + 'Domains being blocked:        ' + Fore.WHITE + response['domains_being_blocked'])
    print(Fore.CYAN + 'Total Queries today:          ' + Fore.WHITE + response['dns_queries_today'])
    print(Fore.CYAN + 'Ads blocked today:            ' + Fore.WHITE + response['ads_blocked_today'])
    print(Fore.CYAN + 'Percentage Queries Blocked:   ' + Fore.WHITE + response['ads_percentage_today'])


status = check_status()

if status == 'enabled':
    while True:
        print(chr(27) + "[2J")
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.RED + ' ▄▄▄·▪   ' + Fore.GREEN + '    ▄ .▄      ▄▄▌  ▄▄▄ .')
        print(Fore.RED + '▐█ ▄███  ' + Fore.GREEN + '   ██▪▐█▪     ██•  ▀▄.▀·') 
        print(Fore.RED + ' ██▀·▐█· ' + Fore.GREEN + '   ██▀▐█ ▄█▀▄ ██▪  ▐▀▀▪▄')
        print(Fore.RED + '▐█▪·•▐█▌ ' + Fore.GREEN + '   ██▌▐▀▐█▌.▐▌▐█▌▐▌▐█▄▄▌')
        print(Fore.RED + '.▀   ▀▀▀ ' + Fore.GREEN + '   ▀▀▀ · ▀█▄▀▪.▀▀▀  ▀▀▀ ')
        print(Fore.WHITE+'\nService: ' + Fore.GREEN+'Active')
        print(Fore.WHITE+'-------------------------------------')
        get_summary()
        time.sleep(30)
else:
    print("Pi-Hole{Fore.RED} not active.")
