import socket
import sys
import datetime

UDP_IP = '127.0.0.1'
global UDP_PORT
UDP_PORT = 2345
BUFF_SIZE = 1024

if __name__ == '__main__':
    if len(sys.argv) == 1:
        UDP_PORT = int(sys.argv[1])
        
    print ("UDP target IP:", UDP_IP)
    print ("UDP targer Port:", UDP_PORT)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Internet UDP
    sock.bind((UDP_IP, UDP_PORT))
    
    while True:
        #get data from client, addr is who sent it (i.e. rpi client)
        sock.listen(9)
        conn, address = soc.accept()
        data, addr = sock.recvfrom(BUFF_SIZE) 
        
