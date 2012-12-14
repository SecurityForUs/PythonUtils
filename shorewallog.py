import re
# Dec 10 09:52:01 MpFw2 Shorewall:net2dmz:ACCEPT: IN=eth0 OUT=eth1 MAC=00:01:03:e4:50:fa:00:02:4b:d3:60:a0:08:00  SRC=67.107.47.65 DST=74.219.74.165 LEN=67 TOS=00 PREC=0x00 TTL=46 ID=0 DF PROTO=UDP SPT=8010 DPT=53 LEN=47
# Regex was tested on myregextester.com
reg = re.compile(r"(\w+\s\d{2}\s\d{2}:\d{2}:\d{2})\s([^\s].+)\sShorewall:([^:]\w+):([^:]\w+):\sIN=([^\s].+)\sOUT=([^\s].+)?\sMAC=([^\s].+)\sSRC=([^\s].+)\sDST=([^\s].+)\sLEN=(\d{1,})\sTOS=([^\s]\w+)\sPREC=([^\s]\w+)\sTTL=(\d{1,})\sID=(\d{1,})\s(\w+\s){1,}PROTO=([^\s]\w+)\sSPT=(\d{1,})\sDPT=(\d{1,})\s(.+)")

# Some test data thrown in to show it works
test = [
    "Dec 10 09:52:01 MpFw2 Shorewall:net2dmz:ACCEPT: IN=eth0 OUT=eth1 MAC=00:01:03:e4:50:fa:00:02:4b:d3:60:a0:08:00  SRC=67.107.47.65 DST=74.219.74.165 LEN=67 TOS=00 PREC=0x00 TTL=46 ID=0 DF PROTO=UDP SPT=8010 DPT=53 LEN=47",
    'Dec 10 09:52:02 MpFw2 Shorewall:net2dmz:ACCEPT: IN=eth0 OUT=eth1 MAC=00:01:03:e4:50:fa:00:02:4b:d3:60:a0:08:00  SRC=170.37.227.17 DST=74.219.74.219 LEN=60 TOS=00 PREC=0x00 TTL=46 ID=59400 CE DF PROTO=TCP SPT=12181 DPT=80 SEQ=4217531116 ACK=0 WINDOW=32768 SYN URGP=0',
    'Dec 10 09:52:02 MpFw2 Shorewall:dmz2net:ACCEPT: IN=eth1 OUT=eth0 MAC=00:04:76:70:fb:ce:00:16:36:1e:85:33:08:00  SRC=74.219.74.164 DST=50.23.136.174 LEN=57 TOS=00 PREC=0x00 TTL=63 ID=38447 CE PROTO=UDP SPT=35277 DPT=53 LEN=37',
    'Dec 10 09:52:03 MpFw2 Shorewall:net2dmz:ACCEPT: IN=eth0 OUT=eth1 MAC=00:01:03:e4:50:fa:00:02:4b:d3:60:a0:08:00  SRC=67.107.47.65 DST=74.219.74.164 LEN=80 TOS=00 PREC=0x00 TTL=46 ID=34291 CE PROTO=UDP SPT=56933 DPT=53 LEN=60',
    'Dec 10 09:52:04 MpFw2 Shorewall:loc2fw:ACCEPT: IN=eth2 OUT= MAC=00:1e:8c:82:8a:65:00:0f:f8:d6:1e:ca:08:00  SRC=172.16.24.85 DST=172.31.1.2 LEN=52 TOS=00 PREC=0x00 TTL=127 ID=4232 DF PROTO=TCP SPT=4085 DPT=22 SEQ=1220379882 ACK=0 WINDOW=65535 SYN URGP=0',
    'This won\'t pass yo'
]

# Loop through each item in 'test'
for item in test:
    # check = match object on success, else None (NULL)
   check = reg.match(item)

    # Only output information on successful matches
   if check:
       print "Groups:",check.groups()
