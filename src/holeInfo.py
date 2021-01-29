#!/usr/bin/python3
import json
import time
import curses
import sys
from urllib.error import URLError
from urllib.request import urlopen

class holeInfo(object):
    
    def __init__(self):
        self.url = "http://pi.hole/admin"

        self.status_check = "%s/api.php?status" % self.url

        self.summary_today = "%s/api.php?summary" % self.url

        self.summaryScreen = curses.initscr()

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(curses.COLOR_RED, curses.COLOR_RED, -1)
        curses.init_pair(curses.COLOR_GREEN, curses.COLOR_GREEN, -1)
        curses.init_pair(curses.COLOR_CYAN, curses.COLOR_CYAN, -1)
        curses.init_pair(curses.COLOR_YELLOW, curses.COLOR_YELLOW, -1)

    def nativeJson(self, data):
        return json.loads(data)


    def request(self, input_url, method='GET'):
        response = urlopen(input_url)
        return self.nativeJson(response.read())


    def checkStatus(self):
        try:
            response = self.request(self.status_check)
        except URLError:
            return False
        return response['status']


    def getSummary(self):
        response = self.request(self.summary_today)
        self.summaryScreen.addstr('Lists updated ' + str(response['gravity_last_updated']['relative']['days']) + " Days " + str(response['gravity_last_updated']['relative']['hours']) + " Hours " + str(response['gravity_last_updated']['relative']['minutes']) + " Minutes ago." + "\n",curses.color_pair(curses.COLOR_YELLOW,))
        self.summaryScreen.addstr('----------------------------------------------' + "\n")
        self.summaryScreen.addstr('Domains being blocked:        ',curses.color_pair(curses.COLOR_CYAN,)) 
        self.summaryScreen.addstr(response['domains_being_blocked'] + "\n")
        self.summaryScreen.addstr('Total queries today:          ',curses.color_pair(curses.COLOR_CYAN,))
        self.summaryScreen.addstr(response['dns_queries_today'] + "\n")
        self.summaryScreen.addstr('DNS queries blocked today:    ',curses.color_pair(curses.COLOR_CYAN,))
        self.summaryScreen.addstr(response['ads_blocked_today'] + "\n")
        self.summaryScreen.addstr('Percentage queries blocked:   ',curses.color_pair(curses.COLOR_CYAN,))
        self.summaryScreen.addstr(response['ads_percentage_today'] + "\n")
        self.summaryScreen.addstr('Unique Domains:               ',curses.color_pair(curses.COLOR_CYAN,))
        self.summaryScreen.addstr(response['unique_domains'] + "\n")
        self.summaryScreen.addstr('Queries Cached:               ',curses.color_pair(curses.COLOR_CYAN,))
        self.summaryScreen.addstr(response['queries_cached'] + "\n")
        self.summaryScreen.addstr('Queries Forwarded:            ',curses.color_pair(curses.COLOR_CYAN,))
        self.summaryScreen.addstr(response['queries_forwarded'] + "\n")
        self.summaryScreen.refresh()
        

    def showBanner(self):
        self.summaryScreen.addstr('    ___       ___   ')
        self.summaryScreen.addstr('    ___       ___       ___       ___   ' + "\n",curses.color_pair(curses.COLOR_RED,))
        self.summaryScreen.addstr('   /\  \     /\  \  ')
        self.summaryScreen.addstr('   /\__\     /\  \     /\__\     /\  \  ' + "\n",curses.color_pair(curses.COLOR_RED,)) 
        self.summaryScreen.addstr('  /::\  \   _\:\  \ ')
        self.summaryScreen.addstr('  /:/__/_   /::\  \   /:/  /    /::\  \ ' + "\n",curses.color_pair(curses.COLOR_RED,))
        self.summaryScreen.addstr(' /::\:\__\ /\/::\__\\')
        self.summaryScreen.addstr(' /::\/\__\ /:/\:\__\ /:/__/    /::\:\__\\'+ "\n",curses.color_pair(curses.COLOR_RED,))
        self.summaryScreen.addstr(' \/\::/  / \::/\/__/')
        self.summaryScreen.addstr(' \/\::/  / \:\/:/  / \:\  \    \:\:\/  /' + "\n",curses.color_pair(curses.COLOR_RED,))
        self.summaryScreen.addstr('    \/__/   \:\__\  ')
        self.summaryScreen.addstr('   /:/  /   \::/  /   \:\__\    \:\/  / ' + "\n",curses.color_pair(curses.COLOR_RED,))
        self.summaryScreen.addstr('             \/__/  ')
        self.summaryScreen.addstr('   \/__/     \/__/     \/__/     \/__/  ' + "\n",curses.color_pair(curses.COLOR_RED,))
        
        status = self.checkStatus()
        if status == 'enabled':
                self.summaryScreen.addstr("Service: ")
                self.summaryScreen.addstr("Active" + "\n",curses.color_pair(curses.COLOR_GREEN,))
                self.getSummary()
        elif status == 'disabled':
                self.summaryScreen.addstr("Service: ")
                self.summaryScreen.addstr("Disabled" + "\n",curses.color_pair(curses.COLOR_RED,))
                self.getSummary()
        elif status == False:
                self.summaryScreen.addstr("\nERROR:piHole not reachable \n",curses.color_pair(curses.COLOR_RED,))
        self.summaryScreen.refresh()

    def main(self, sleep_interval):
        try:
            while True:
                self.summaryScreen.clear()
                self.showBanner()
                time.sleep(sleep_interval)
        except KeyboardInterrupt as e:
            print("Keyboard Interrupt. Quitting.")
            curses.endwin()
            exit()
    
if __name__ == "__main__":
    info = holeInfo()
    if len(sys.argv) > 1 and sys.argv[1] == "-s":
        info.main(sleep_interval=int(sys.argv[2]))
    else:
        info.main(sleep_interval=30)