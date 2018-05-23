import json
import time
from urllib.request import urlopen
from colorama import Fore

url = "http://pi.hole/admin"

password = "f8e70093b605c8fcec1534a5e3da88e2c5e028fe60eec09bd12c9c33d5be4c04"

status_check = "%s/api.php?status&auth=%s" % (url, password)

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
    print(f'{Fore.CYAN}Domains being blocked: {Fore.WHITE}' + response['domains_being_blocked'])
    print(f'{Fore.CYAN}Total Queries today: {Fore.WHITE}' + response['dns_queries_today'])
    print(f'{Fore.CYAN}Ads blocked today: {Fore.WHITE}' + response['ads_blocked_today'])
    print(f'{Fore.CYAN}Percentage Queries Blocked {Fore.WHITE}' + response['ads_percentage_today'])


status = check_status()

if status == 'enabled':
    while True:
        print(chr(27) + "[2J")
        print(f'\n{Fore.RED}    ____  _  {Fore.GREEN}     __  __      __ ')  
        print(f' {Fore.RED}  / __ \(_)   {Fore.GREEN}  / / / /___  / /__ ')
        print(f'{Fore.RED}  / /_/ / /{Fore.WHITE}_____{Fore.GREEN}/ /_/ / __ \/ / _ \ ')
        print(f'{Fore.RED} / ____/ /{Fore.WHITE}_____{Fore.GREEN}/ __  / /_/ / /  __/ ')
        print(f'{Fore.RED}/_/   /_/    {Fore.GREEN} /_/ /_/\____/_/\___/ ')
        print(f'\n{Fore.WHITE}Service: {Fore.GREEN}Active')
        print(f'{Fore.WHITE}----------------------------------')
        get_summary()
        time.sleep(20)
else:
    print("Pi-Hole{Fore.RED} not active.")
