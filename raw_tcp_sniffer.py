__author__ = 'bobby'

import struct
import socket
import dicts


def tcp(ptk):
    tcpHeader = ptk[0][34:54]
    tcp_hdr = struct.unpack("!HHLL1sBHHH", tcpHeader)  # HH 2 short integers 1 for each port, 16B for trash
    print 'TCP Header:'+'\n'+'Source port: {}  Destination port: {}  Sequence Number: {}  ACK Number:  {}  '.format(*tcp_hdr[:4])
    print 'TCP Flags: '+dicts.flag_dict[str(hex(tcp_hdr[5]))]
    print 'Window: {}  Checksum: {}  Urgent Pointer: {}'.format(*tcp_hdr[6:])
    # HTTP data
    if tcp_hdr[0] == 80 or tcp_hdr[0] == 443:  # or tcp_hdr[1] == 80 or tcp_hdr[1] == 443
        data = ptk[0][58:]
        print "HTTP (user-agent and data) : "+'\n'+data+'\n'+'-'*25


def udp(ptk):
    udp_datagram = ptk[0][34:38]
    udp_hdr = struct.unpack("!HHHH", udp_datagram)
    print "UDP Header:"+'\n'+"Source port: {}  Destiny port: {}  length: {}  checksum: {}".format(*udp_hdr)+'\n'+'-'*25


def icmp(ptk):
    icmp_header = ptk[0][34:38]
    icmp_hdr = struct.unpack("!BBH", icmp_header)
    print "ICMP Header:"+'\n'+'Type: {}  Code:  {}  checksum:  {}'.format(*icmp_hdr)+'\n'+'Data: '+ptk[0][38:42]+'\n'+\
          '-'*25

# Captures the incoming and outgoing connections.
# Create a new socket using the given address family, socket type and protocol number, 0x0003 -> all protocols
try:
    rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))  # 0x0800 -> IP (only incoming)

    while 1:
        # Receive data from the socket
        ptk = rawSocket.recvfrom(65565)  # returns the data into a tuple

        'The Ethernet header'
        ethernetHeader = ptk[0][0:14]  # 14 Bytes Ethernet header (first element, the first 14 bytes of it)
        eth_hdr = struct.unpack("!6s6sH", ethernetHeader)  # 6B dst_mac address , 6B src_mac address, 2B ether_type

        if socket.ntohs(eth_hdr[2]) == 8:  # IP
            'The IP header'
            ipHeader = ptk[0][14:34]  # 20 Bytes IP header
            ip_hdr = struct.unpack("!9sB2s4s4s", ipHeader)  # 12+4+4 = 20-> 12 trash, 4B srcAdrss, 4B dstAdrr

            if ip_hdr[1] == 6:  # TCP
                'The TCP header'
                tcp(ptk)

            elif ip_hdr[1] == 16:  # UDP
                'The UDP header'
                udp(ptk)

            elif ip_hdr[1] == 1:  # ICMP
                'The ICMP header'
                icmp(ptk)

    rawSocket.close()
except socket.error:
    print "Need to be root to run the socket!"