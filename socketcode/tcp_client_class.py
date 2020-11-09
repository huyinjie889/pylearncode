import socket
import subprocess

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
        self.tcp_client.send(msg.encode("utf-8"))

    def recv(self):
        rec = self.tcp_client.recv(self._buffersize).decode("utf-8")
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
    ipport = ("146.56.194.21",8080)
    backlog = 5
    buffersize = 1024

    myclient1 = Tcp_Client(ipport,backlog,buffersize)
    myclient1.conn()
    while True:
        cmd = input("请输入命令:")
        if not cmd:continue
        myclient1.send(cmd)
        if cmd == 'exit':
            break
        length = int(myclient1.recv())
        myclient1.send('ready')
        rec_size = 0
        rec_msg = ''
        if rec_size < length:
            rec_msg += myclient1.recv()
            rec_size = len(rec_msg)
        print(rec_msg)
    myclient1.close()

if __name__ == '__main__':
    main()

