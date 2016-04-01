import struct, socket, sys, time, os
from sickbeard import logger
from urlparse import urlparse

#Test Connection function
def testCon(host):
        o = urlparse(host)
        s = socket.socket()
        s.settimeout(1)
        try:
            s.connect((o.hostname, o.port))
            return "Up"
            s.close()
        except socket.error, e:
            return "Down"

#Wake function
def wakeOnLan(ethernet_address):

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
        
def wakeHost(mac, host, retries=5, timeout=20):
    
        i = 0
        logger.log(u"Testing connectivity to host", logger.DEBUG)
        while testCon(host) == "Down" and i < retries:
            logger.log(u"host seems to be down - sending magic packet", logger.DEBUG)
            wakeOnLan(mac)    
            time.sleep(timeout)
            i = i + 1
            
        if testCon(host) == "Down":
            logger.log(u"host unreachable after sending "+retries+" magic packets - check if host is running", logger.INFO)
        
