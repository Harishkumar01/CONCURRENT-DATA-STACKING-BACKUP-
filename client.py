import socket
import sys
import os
import struct
import paho.mqtt.client as paho

TCP_IP = "127.0.0.1"
TCP_PORT = 12346
BUFFER_SIZE = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = paho.Client()
client.connect("broker.mqttdashboard.com",1883 )

def conn():
    print("Sending server request...")
    try:
        s.connect((TCP_IP, TCP_PORT))
        print ("Connection sucessful")
    except:
        print ("Connection unsucessful. Make sure the server is online.")

def upld(file_name):
    print ("\nUploading file: {}...".format(file_name))
    try:
        content = open(file_name, "rb")
    except:
        print("Couldn't open file. Make sure the file name was entered correctly.")
        return
    try:
        s.send("UPLD")
    except:
        print( "Couldn't make server request. Make sure a connection has been established.")
        return
    try:
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name)
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("i", os.path.getsize(file_name)))
    except:
        print("Error sending file details")
    try:
        l = content.read(BUFFER_SIZE)
        print ("\nSending...")
        while l:
            s.send(l)
            l = content.read(BUFFER_SIZE)
        content.close()
        upload_time = struct.unpack("f", s.recv(4))[0]
        upload_size = struct.unpack("i", s.recv(4))[0]
        print ("\nSent file: {}\nTime elapsed: {}s\nFile size: {}b".format(file_name, upload_time, upload_size))
    except:
        print ("Error sending file")
        return
    return

def on_message(client,userdata,msg):
    print((msg.payload).decode("utf-8"))
    a = (msg.payload).decode("utf-8")
    if(a == "back"):
        upld("filee")

def subscribe_get_message():
    client.subscribe("topic/1",qos=1)
    client.on_message = on_message
    client.loop_forever()

conn()
subscribe_get_message()
