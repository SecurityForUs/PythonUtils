import re
import argparse

# Dec 10 09:52:01 MpFw2 Shorewall:net2dmz:ACCEPT: IN=eth0 OUT=eth1 MAC=00:01:03:e4:50:fa:00:02:4b:d3:60:a0:08:00  SRC=67.107.47.65 DST=74.219.74.165 LEN=67 TOS=00 PREC=0x00 TTL=46 ID=0 DF PROTO=UDP SPT=8010 DPT=53 LEN=47
# Regex was tested on myregextester.com
#reg = re.compile(r"(\w+\s\d{2}\s\d{2}:\d{2}:\d{2})\s([^\s].+)\sShorewall:([^:]\w+):([^:]\w+):\sIN=([^\s].+)\sOUT=([^\s].+)?\sMAC=([^\s].+)\sSRC=([^\s].+)\sDST=([^\s].+)\sLEN=(\d{1,})\sTOS=([^\s]\w+)\sPREC=([^\s]\w+)\sTTL=(\d{1,})\sID=(\d{1,})\s(\w+\s){1,}PROTO=([^\s]\w+)\sSPT=(\d{1,})\sDPT=(\d{1,})\s(.+)")

# Some test data thrown in to show it works
"""
test = [
    "Dec 10 09:52:01 MpFw2 Shorewall:net2dmz:ACCEPT: IN=eth0 OUT=eth1 MAC=00:01:03:e4:50:fa:00:02:4b:d3:60:a0:08:00  SRC=67.107.47.65 DST=74.219.74.165 LEN=67 TOS=00 PREC=0x00 TTL=46 ID=0 DF PROTO=UDP SPT=8010 DPT=53 LEN=47",
    'Dec 10 09:52:02 MpFw2 Shorewall:net2dmz:ACCEPT: IN=eth0 OUT=eth1 MAC=00:01:03:e4:50:fa:00:02:4b:d3:60:a0:08:00  SRC=170.37.227.17 DST=74.219.74.219 LEN=60 TOS=00 PREC=0x00 TTL=46 ID=59400 CE DF PROTO=TCP SPT=12181 DPT=80 SEQ=4217531116 ACK=0 WINDOW=32768 SYN URGP=0',
    'Dec 10 09:52:02 MpFw2 Shorewall:dmz2net:ACCEPT: IN=eth1 OUT=eth0 MAC=00:04:76:70:fb:ce:00:16:36:1e:85:33:08:00  SRC=74.219.74.164 DST=50.23.136.174 LEN=57 TOS=00 PREC=0x00 TTL=63 ID=38447 CE PROTO=UDP SPT=35277 DPT=53 LEN=37',
    'Dec 10 09:52:03 MpFw2 Shorewall:net2dmz:ACCEPT: IN=eth0 OUT=eth1 MAC=00:01:03:e4:50:fa:00:02:4b:d3:60:a0:08:00  SRC=67.107.47.65 DST=74.219.74.164 LEN=80 TOS=00 PREC=0x00 TTL=46 ID=34291 CE PROTO=UDP SPT=56933 DPT=53 LEN=60',
    'Dec 10 09:52:04 MpFw2 Shorewall:loc2fw:ACCEPT: IN=eth2 OUT= MAC=00:1e:8c:82:8a:65:00:0f:f8:d6:1e:ca:08:00  SRC=172.16.24.85 DST=172.31.1.2 LEN=52 TOS=00 PREC=0x00 TTL=127 ID=4232 DF PROTO=TCP SPT=4085 DPT=22 SEQ=1220379882 ACK=0 WINDOW=65535 SYN URGP=0',
    'This won\'t pass yo'
]
"""
# Initiate the argument parser
args = argparse.ArgumentParser(description='Shorewall/Netfilter log viewer/filterer/etc...', epilog="Regex is supported for any entries")

args.add_argument("-da", "--date", help="The date to search for (format: MMM dd HH:MM:SS ie: Dec 09 13:58:01)")
args.add_argument("-H", "--host", help="Hostname to search for")
args.add_argument("-i", "--ina", help="Input device (eth0, wlan0, eth10, etc...)")
args.add_argument("-o", "--out", help="Output device (eth0, wlan0, eth10, etc...)")
args.add_argument("-s", "--source", help="Source IP (IPv4 so far only)")
args.add_argument("-d", "--destination", help="Destination IP")
args.add_argument("-z", "--zone", help="Firewall zone (net2dmz, loc2fw, etc...)")
args.add_argument("-st", "--status", help="ACCEPT, DROP, etc...")
args.add_argument("-m", "--mac", help="MAC address of device")
args.add_argument("-l", "--len", help="Packet length")
args.add_argument("-t", "--tos", help="TOS")
args.add_argument("-prec", "--prec", help="I don't know...")
args.add_argument("-ttl", "--ttl", help="Time to live for packet")
args.add_argument("-p", "--proto", help="Protocol (TCP, UDP, ICMP, etc...)")
args.add_argument("-sp", "--sport", help="Source port of record")
args.add_argument("-dp", "--dport", help="Destination port of record")

args = args.parse_args()

if args.date is None:
    args.date = "\w+\s\d{2}\s\d{2}:\d{2}:\d{2}"

if args.host is None:
    args.host = "[^\s].+"

if args.zone is None:
    args.zone = "[^:]\w+"

if args.status is None:
    args.status = "[^:]\w+"

if args.ina is None:
    args.ina = "[^\s].+"

if args.out is None:
    args.out = "[^\s].+"

if args.mac is None:
    args.mac = "[^\s].+"

if args.source is None:
    args.source = "[^\s].+"

if args.destination is None:
    args.destination = "[^\s].+"

if args.len is None:
    args.len = "\d{1,}"

if args.tos is None:
    args.tos = "[^\s]\w+"

if args.prec is None:
    args.prec = "[^\s]\w+"

if args.ttl is None:
    args.ttl = "\d{1,}"

if args.proto is None:
    args.proto = "[^\s]\w+"

if args.sport is None:
    args.sport = "\d{1,}"

if args.dport is None:
    args.dport = "\d{1,}"

reg = re.compile(r"(%s)\s(%s)\sShorewall:(%s):(%s):\sIN=(%s)\sOUT=(%s)?\sMAC=(%s)\sSRC=(%s)\sDST=(%s)\sLEN=(%s)\sTOS=(%s)\sPREC=(%s)\sTTL=(%s)\sID=(\d{1,})\s(\w+\s){1,}PROTO=(%s)\sSPT=(%s)\sDPT=(%s)\s(.+)" % (args.date, args.host, args.zone, args.status, args.ina, args.out, args.mac, args.source, args.destination, args.len, args.tos, args.prec, args.ttl, args.proto, args.sport, args.dport))

files = [ "/var/log/messages", "/var/log/ulogd/shorewall.log" ]

# Loop through each item in 'test'
for fil in files:
    try:
        with open(fil, "r") as filo:
            content = filo.read()
            for check in reg.finditer(content):
                val = check.groups()
                msg = "%s %s Shorewall:%s:%s:" % (val[0], val[1], val[2], val[3])
                msg = "%s IN=%s OUT=%s MAC=%s SRC=%s" % (msg, val[4], val[5], val[6], val[7])
                msg = "%s DST=%s LEN=%s TOS=%s PREC=%s" % (msg, val[8], val[9], val[10], val[11])
                msg = "%s TTL=%s ID=%s %s PROTO=%s" % (msg, val[12], val[13], val[14], val[15])
                msg = "%s SPT=%s DPT=%s %s" % (msg, val[16], val[17], val[18])
                print msg

            filo.close()
    except IOError:
        print "%s does not exist or unable to be read" % (fil)
