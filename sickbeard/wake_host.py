import struct, socket, sys, time, os

from urlparse import urlparse

    #Test Connection function
def TestCon(host):
        o = urlparse(host)
        s = socket.socket()
        s.settimeout(1)
        try:
            s.connect((o.hostname,o.port))
            return "Up"
            s.close()
        except socket.error, e:
            return "Down"

#Wake function
def WakeOnLan(ethernet_address):

        addr_byte = ethernet_address.split(':')
        hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
        int(addr_byte[1], 16),
        int(addr_byte[2], 16),
        int(addr_byte[3], 16),
        int(addr_byte[4], 16),
        int(addr_byte[5], 16))
                     
        # Build the Wake-On-LAN "Magic Packet"...
                        
        msg = '\xff' * 6 + hw_addr * 16
                           
        # ...and send it to the broadcast address using UDP
                              
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        ss.sendto(msg, ('<broadcast>', 9))
        ss.close()
        
def WakeHost(mac, host, retries, timeout):
    
    i=1
    logger.log(u"Testing connectivity to host %s" % host)
    while TestCon(host)=="Down" and i<retries+1:
        i=i+1
        logger.log(u"host seems to be down - sending magic packet")
        WakeOnLan(mac)    
        time.sleep(timeout)
        