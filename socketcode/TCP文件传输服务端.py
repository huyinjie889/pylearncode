import socket
import struct
import json

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("127.0.0.1",8005))
server.listen()
buffersize = 2048
conn,addr = server.accept()

#接收服务端发来的报头
msg = conn.recv(4)
packet_length = struct.unpack("i",msg)[0]
json_head =conn.recv(packet_length).decode("utf-8")
filehead = json.loads(json_head)
filename = filehead["filename"]
filesize = filehead["filesize"]
#接收文件
with open (filename,'wb') as f:
    while buffersize < filesize:
        content = conn.recv(buffersize)
        f.write(content)
        filesize -= buffersize
    content = conn.recv(buffersize)
    f.write(content)
f.close()

