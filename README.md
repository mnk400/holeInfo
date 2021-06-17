## Pi-Hole Status

Command-line utility to display pi-hole statistics in your terminal without having to login or setting up any additional confirmation. 
![](img/terminal-screenshot.png)

Script updates every 30 seconds by default, `-s` can be specified to change the update
timer like `holeinfo -s 5`.

Option `-ip` can be specified to supply a custom IP address/URL to the script like `holeinfo -ip 192.168.1.64`, by default the script will attempt to reach pi.hole domain which is usually automatically configured when installing piHole.

Can be installed using pip:
```
pip3 install holeinfo
```

Installing from source:
```
git clone https://github.com/mnk400/holeinfo
cd holeinfo
python3 build.py install
```

Usage:
```
$ holeinfo
```


