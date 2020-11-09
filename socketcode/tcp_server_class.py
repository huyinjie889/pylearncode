import socket
import subprocess

class Tcp_Server():
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
        self.tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp_server.bind(self._ipport)
        self.tcp_server.listen(self._backlog)
        self.conn,self.addr = self.tcp_server.accept()

    def send(self,msg):
        self.conn.send(msg.encode("utf-8"))

    def recv(self):
        rec = self.conn.recv(self._buffersize).decode("utf-8")
        return rec

    def exec_cmd(self,cmd):
        res = subprocess.Popen(cmd,shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        err = res.stderr.read()
        if err:
            cmd_res = err
        else:
            cmd_res = res.stdout.read()
        return cmd_res.decode("utf-8")

    def close(self):
        self.conn.close()


def main():
    ipport = ("127.0.0.1",8007)
    backlog = 5
    buffersize = 1024
    myserver1 = Tcp_Server(ipport, backlog, buffersize)
    myserver1.conn()
    while True:
        rec = myserver1.recv()
        if rec == 'exit':
            break
        cmd_res = myserver1.exec_cmd(rec)
        print(cmd_res)
        length = str(len(cmd_res))
        myserver1.send(length)
        rec = myserver1.recv()
        if rec == 'ready':
            myserver1.send(cmd_res)
    myserver1.close()

if __name__ == '__main__':
    main()






