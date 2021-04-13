import socket
import threading
import pickle
from packet import *
import sys

class Client:
    def __init__(self,server_host,server_port):
        self.server_host=server_host
        self.server_port=server_port
        self.socket=socket.socket(socket.AF_INET , socket.SOCK_DGRAM )
        self.active=False
        self.clients=0
        self.filed=0
        self.files=[]
    def download(self,firstPckt):
        file=open("File-"+str(self.filed)+".csv",'wb')
        pckt=firstPckt
        while pckt.flag=="TR":
            file.write(pckt.data)
            pckt=pickle.loads(self.socket.recvfrom(4096)[0])
        file.close()
        self.filed+=1
        return pckt


    def rec(self):
        afterDw=False
        while self.active:
            if(not afterDw):
                msg=pickle.loads(self.socket.recvfrom(4096)[0])
                afterDw=False
            if(msg.flag=="GRT"):
                self.files=msg.data["files"]
            elif(msg.flag=="UPD"):
                self.clients=msg.data["users"]
            elif(msg.flag=="TR"):
                msg=self.download(msg)
                afterDw=True
            print("Server: ",msg.data)
    
    def start(self):
        self.active=True
        hello_msg={'type':'init'}
        helloPckt=Packet(data=hello_msg,flag="INIT")
        self.socket.sendto(pickle.dumps(helloPckt),(self.server_host,self.server_port))
        rec_thread=threading.Thread( target = self.rec )
        rec_thread.start()
        print("================Client Starting==============")
        try:
            while self.active:
                print("Files: ",self.files)
                print("Users: ",self.clients)
                print("1)Transfer File\n2)Close Connection")
                opt = int(input("Option: "))
                if(opt==1):
                    users=int(input("How many users?"))
                    req_msg={"type":"req","file":"file_test.txt","users":users}
                    req_pckt=Packet(req_msg,flag="RQ")
                    self.socket.sendto(pickle.dumps(req_pckt),(self.server_host,self.server_port))
                elif(opt==2):
                    bye_msg={"type":"bye"}
                    bye_pckt=Packet(bye_msg,flag="BYE")
                    self.socket.sendto(pickle.dumps(bye_pckt),(self.server_host,self.server_port))
                    self.active=False
                else:
                    print("Select  valid option")
        except:
            bye_msg={"type":"bye"}
            bye_pckt=Packet(bye_msg,flag="BYE")
            self.socket.sendto(pickle.dumps(bye_pckt),(self.server_host,self.server_port))                    
        self.socket.close()
        sys.exit(0)


if __name__=="__main__":
    host=input("Server Host: ")        
    port=int(input("Server Port: "))
    client=Client(host,port)
    client.start()