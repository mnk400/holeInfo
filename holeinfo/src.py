import json
import time
import argparse
from urllib.error import URLError
from urllib.request import urlopen

try:
    import curses
except ImportError:
    import platform

    if platform.system() == "Windows":
        print(
            "Curses not installed on windows system,\nRun `pip install windows-curses`."
        )
        exit(1)
    else:
        print("Unable to import curses.")
        exit(1)


class holeInfo(object):

    def __init__(self, ip: str, api_key: str = None, update_interval: int = 30):
        self.api_key = api_key
        self.update_interval = update_interval
        self.url = "http://%s/admin" % ip
        self.status_check = "%s/api.php?status" % self.url
        self.summary_today = "%s/api.php?summary" % self.url
        self.enable_pi = "%s/api.php?enable&auth=%s" % (self.url, api_key)
        self.disable_pi = "%s/api.php?disable&auth=%s" % (self.url, api_key)
        if api_key:
            self.top_domains = "%s/api.php?topItems&auth=%s" % (self.url, api_key)
            self.query_sources = "%s/api.php?getQuerySources&auth=%s" % (self.url, api_key)

    def nativeJson(self, data):
        return json.loads(data)

    def request(self, input_url, method="GET"):
        response = urlopen(input_url)
        return self.nativeJson(response.read())

    def checkStatus(self):
        try:
            response = self.request(self.status_check)
        except URLError:
            return False
        return response["status"]

    def getSummary(self):
        response = self.request(self.summary_today)
        self.summaryScreen.addstr(
            "Lists updated "
            + str(response["gravity_last_updated"]["relative"]["days"])
            + " Days "
            + str(response["gravity_last_updated"]["relative"]["hours"])
            + " Hours "
            + str(response["gravity_last_updated"]["relative"]["minutes"])
            + " Minutes ago."
            + "\n",
            curses.color_pair(
                curses.COLOR_YELLOW,
            ),
        )
        self.summaryScreen.addstr(
            "----------------------------------------------" + "\n"
        )
        self.summaryScreen.addstr(
            "Domains being blocked:        ",
            curses.color_pair(
                curses.COLOR_CYAN,
            ),
        )
        self.summaryScreen.addstr(response["domains_being_blocked"] + "\n")
        self.summaryScreen.addstr(
            "Total queries today:          ",
            curses.color_pair(
                curses.COLOR_CYAN,
            ),
        )
        self.summaryScreen.addstr(response["dns_queries_today"] + "\n")
        self.summaryScreen.addstr(
            "DNS queries blocked today:    ",
            curses.color_pair(
                curses.COLOR_CYAN,
            ),
        )
        self.summaryScreen.addstr(response["ads_blocked_today"] + "\n")
        self.summaryScreen.addstr(
            "Percentage queries blocked:   ",
            curses.color_pair(
                curses.COLOR_CYAN,
            ),
        )
        self.summaryScreen.addstr(response["ads_percentage_today"] + "\n")
        self.summaryScreen.addstr(
            "Unique Domains:               ",
            curses.color_pair(
                curses.COLOR_CYAN,
            ),
        )
        self.summaryScreen.addstr(response["unique_domains"] + "\n")
        self.summaryScreen.addstr(
            "Queries Cached:               ",
            curses.color_pair(
                curses.COLOR_CYAN,
            ),
        )
        self.summaryScreen.addstr(response["queries_cached"] + "\n")
        self.summaryScreen.addstr(
            "Queries Forwarded:            ",
            curses.color_pair(
                curses.COLOR_CYAN,
            ),
        )
        self.summaryScreen.addstr(response["queries_forwarded"] + "\n")
        self.summaryScreen.refresh()

    def getDomains(self, url, title, dict_key, limit=3):
        response = self.request(url)
        if not response:
            response = {dict_key: {"Error Loading Data": -1}}
        title_str = title + ":" + " "*(29-len(title))
        self.summaryScreen.addstr(
            title_str,
            curses.color_pair(
                curses.COLOR_CYAN,
            ),
        )
        self.summaryScreen.addstr(list(response[dict_key].keys())[0] + "\n")
        for i in range(1, min(limit, len(response[dict_key]))):
            self.summaryScreen.addstr(
                 "                              " +
                 list(response[dict_key].keys())[i] +
                 "\n"
            )

    def showBanner(self):
        self.summaryScreen.addstr("    ___       ___   ")
        self.summaryScreen.addstr(
            "    ___       ___       ___       ___   " + "\n",
            curses.color_pair(
                curses.COLOR_RED,
            ),
        )
        self.summaryScreen.addstr("   /\  \     /\  \  ")
        self.summaryScreen.addstr(
            "   /\__\     /\  \     /\__\     /\  \  " + "\n",
            curses.color_pair(
                curses.COLOR_RED,
            ),
        )
        self.summaryScreen.addstr("  /::\  \   _\:\  \ ")
        self.summaryScreen.addstr(
            "  /:/__/_   /::\  \   /:/  /    /::\  \ " + "\n",
            curses.color_pair(
                curses.COLOR_RED,
            ),
        )
        self.summaryScreen.addstr(" /::\:\__\ /\/::\__\\")
        self.summaryScreen.addstr(
            " /::\/\__\ /:/\:\__\ /:/__/    /::\:\__\\" + "\n",
            curses.color_pair(
                curses.COLOR_RED,
            ),
        )
        self.summaryScreen.addstr(" \/\::/  / \::/\/__/")
        self.summaryScreen.addstr(
            " \/\::/  / \:\/:/  / \:\  \    \:\:\/  /" + "\n",
            curses.color_pair(
                curses.COLOR_RED,
            ),
        )
        self.summaryScreen.addstr("    \/__/   \:\__\  ")
        self.summaryScreen.addstr(
            "   /:/  /   \::/  /   \:\__\    \:\/  / " + "\n",
            curses.color_pair(
                curses.COLOR_RED,
            ),
        )
        self.summaryScreen.addstr("             \/__/  ")
        self.summaryScreen.addstr(
            "   \/__/     \/__/     \/__/     \/__/  " + "\n",
            curses.color_pair(
                curses.COLOR_RED,
            ),
        )

        status = self.checkStatus()
        if status == "enabled":
            self.summaryScreen.addstr("Service: ")
            self.summaryScreen.addstr(
                "Active" + "\n",
                curses.color_pair(
                    curses.COLOR_GREEN,
                ),
            )
            self.getSummary()
            if self.api_key:
                self.getDomains(self.top_domains, "Top Blocked Domains", "top_ads")
                self.getDomains(self.query_sources, "Top Devices", "top_sources")
        elif status == "disabled":
            self.summaryScreen.addstr("Service: ")
            self.summaryScreen.addstr(
                "Disabled" + "\n",
                curses.color_pair(
                    curses.COLOR_RED,
                ),
            )
        elif status is False:
            self.summaryScreen.addstr(
                "\nERROR:piHole not reachable at %s\n" % self.url,
                curses.color_pair(
                    curses.COLOR_RED,
                ),
            )
        self.summaryScreen.refresh()

    def enable(self):
        if not self.api_key:
            print("API key needed to enable Pi-Hole")
            exit(1)
        if self.checkStatus() == "disabled":
            response = self.request(self.enable_pi)
            if response and response["status"] == "enabled":
                print("PiHole enabled")
            else:
                print("Error enabling piHole")
                exit(1)
        elif self.checkStatus() == "enabled":
            print("PiHole already enabled")
        else:
            print("Error reading PiHole at %s" % self.url)
            exit(1)

    def disable(self):
        if not self.api_key:
            print("API key needed to disable Pi-Hole")
            exit(1)
        if self.checkStatus() == "enabled":
            response = self.request(self.disable_pi)
            if response and response["status"] == "disabled":
                print("PiHole disabled")
            else:
                print("Error disabling piHole")
                exit(1)
        elif self.checkStatus() == "disabled":
            print("PiHole already disabled")
        else:
            print("Error reading PiHole at %s" % self.url)
            exit(1)

    def main(self):
        self.summaryScreen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(curses.COLOR_RED, curses.COLOR_RED, -1)
        curses.init_pair(curses.COLOR_GREEN, curses.COLOR_GREEN, -1)
        curses.init_pair(curses.COLOR_CYAN, curses.COLOR_CYAN, -1)
        curses.init_pair(curses.COLOR_YELLOW, curses.COLOR_YELLOW, -1)

        try:
            try:
                while True:
                    self.summaryScreen.clear()
                    self.showBanner()
                    time.sleep(self.update_interval)
            except KeyboardInterrupt:
                print("Keyboard Interrupt. Quitting.")
                curses.endwin()
                exit()
        except Exception as e:
            curses.endwin()
            print(e)
            exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="holeinfo",
        description="Display pi.hole statistics in your terminal."
    )
    parser.add_argument(
        "--s",
        type=int,
        default=30,
        dest="update_interval",
        help="Time between refreshes(in seconds)",
    )
    parser.add_argument(
        "--api",
        type=str,
        default=None,
        dest="api_key",
        help="API key for pi.hole"
    )
    parser.add_argument(
        "--ip",
        type=str,
        default="pi.hole",
        dest="ip",
        help="Custon URL or IP for your piHole if pi.hole isn't configured on your piHole.",
    )
    parser.add_argument(
        "--enable",
        const=1,
        default=0,
        dest="enable",
        action='store_const',
        help="Enable pi.hole service",
    )
    parser.add_argument(
        "--disable",
        const=1,
        default=0,
        dest="disable",
        action='store_const',
        help="Disable pi.hole service",
    )
    args = parser.parse_args()
    info = holeInfo(args.ip, args.api_key, args.update_interval)
    if args.enable == 1:
        info.enable()
    elif args.disable == 1:
        info.disable()
    else:
        info.main()

main()
