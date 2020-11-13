import socket
import struct
import os
import json

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("127.0.0.1",8005))
buffersize = 2048

#自定义包头并将报头转换为json格式
filehead = {"filename":r"文件操作复习.ev4-【昕昕网络教程-www.xinxin2019.com】.mp4",
            "filedir":r"/Users/huyinjie/Downloads/day28/",
            "filesize":None}
filepath = os.path.join(filehead["filedir"]+filehead["filename"])
filesize = os.path.getsize(filepath)
filehead["filesize"] = filesize
json_head = json.dumps(filehead)

#将报头struct化，然后发送给服务端
packet_length = struct.pack("i",len(json_head))
client.send(packet_length)
client.send(json_head.encode("utf-8"))
#传输文件
with open (filepath,'rb') as f:
    while buffersize < filesize:
        content = f.read(buffersize)
        client.send(content)
        filesize -= buffersize
    content = f.read(buffersize)
    client.send(content)
client.close()



