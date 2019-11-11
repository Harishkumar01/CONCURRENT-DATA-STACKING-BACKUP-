import socket
import time
import struct

print ("\nWelcome to the FTP server.\n\nTo get started, connect a client.")

TCP_IP = "127.0.0.1"
TCP_PORT = 12346
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()

print ("\nConnected to by address: {}".format(addr))

def upld():
    conn.send("1")
    file_name_size = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_size)
    conn.send("1")
    file_size = struct.unpack("i", conn.recv(4))[0]
    start_time = time.time()
    output_file = open(file_name, "wb")
    bytes_recieved = 0
    print ("\nRecieving...")
    while bytes_recieved < file_size:
        l = conn.recv(BUFFER_SIZE)
        output_file.write(l)
        bytes_recieved += BUFFER_SIZE
    output_file.close()
    print ("\nRecieved file: {}".format(file_name))
    conn.send(struct.pack("f", time.time() - start_time))
    conn.send(struct.pack("i", file_size))
    return

while True:
    print ("\n\nWaiting for instruction")
    data = conn.recv(BUFFER_SIZE)
    print ("\nRecieved instruction: {}".format(data))
    if data == "UPLD":
        upld()
    data = None
