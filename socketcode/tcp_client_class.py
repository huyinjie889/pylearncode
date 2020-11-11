import socket
import subprocess
import struct

class Tcp_Client():
    def __init__(self,ipport,backlog,buffersize):
        self._ipport = ipport
        self._backlog = backlog
        self._buffersize = buffersize

    @property
    def ipport(self):
        return self._ipport

    @ipport.setter
    def ipport(self,ipport):
        self._ipport = ipport

    def conn(self):
        self.tcp_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp_client.connect(self._ipport)

    def send(self,msg):
        self.tcp_client.send(msg)

    def recv(self,buffersize):
        rec = self.tcp_client.recv(buffersize)
        return rec

    def exec_cmd(self,cmd):
        res = subprocess.Popen(cmd,shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        err = res.stderr.read()
        if err:
            cmd_res = err
        else:
            cmd_res = res.stdout.read()
        return cmd_res

    def close(self):
        self.tcp_client.close()



def main():
    ipport = ("127.0.0.1",8007)
    backlog = 5
    buffersize = 1024

    myclient1 = Tcp_Client(ipport,backlog,buffersize)
    myclient1.conn()
    while True:
        cmd = input("请输入命令:")
        if not cmd:continue
        myclient1.send(cmd.encode("utf-8"))
        if cmd == 'exit':
            break
        length = struct.unpack("i",myclient1.recv(4))[0]
        rec_size = 0
        rec_msg = b''
        if rec_size < length:
            rec_msg += myclient1.recv(length)
            rec_size = len(rec_msg)
        print(rec_msg.decode("utf-8"))
    myclient1.close()

if __name__ == '__main__':
    main()

