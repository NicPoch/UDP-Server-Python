import socket
import threading
import pickle
from packet import *
import sys

class Server:
    def __init__(self,host="localhost",port=3000):
        self.host=host
        self.port=port
        self.socket=socket.socket(socket.AF_INET , socket.SOCK_DGRAM )
        self.socket.bind((self.host,self.port))
        self.clients=[]
        self.files=[]
        self.queue=[]
        self.processes=0
    
    #updates the state of the application to the users
    def updateUsers(self):
        update_msg={"type":"update","users":len(self.clients),"queue":self.queue}
        update_pckt=Packet(update_msg,flag="UPD")
        for user in self.clients:
            self.socket.sendto(pickle.dumps(update_pckt),(user[0],user[1]))
    #greets a user
    #TODO: select files from directory and sending their info
    def greetUser(self,user):
        greet_msg={"type":"greet","files":[{"nombre":"file_prueba","size":1000}]}
        greet_pckt=Packet(greet_msg,flag="GRT")
        self.socket.sendto(pickle.dumps(greet_pckt),(user[0],user[1]))

    def divideFile(self, mss, filename):
        pckts = []
        with open("news-week-17aug24.csv", "rb") as binary_file:
            data = binary_file.read()
            i = 0
            length = sys.getsizeof(data)
            while i <= length:
                binary_file.seek(i)  # Go to beginning
                couple_bytes = binary_file.read(mss)
                pckts.append(Packet(couple_bytes,hash(couple_bytes)))
                i += mss
        return pckts
    #rtansfers the file to the i users requiered
    #TODO: finish
    def transfer(self,p):
        pckts=self.divideFile(1000,p["file"])
        for i in range(p["users"]):
            user=self.clients[i]
            for pckt in pckts:
                self.socket.sendto(pickle.dumps(pckt),(user[0],user[1]))
    #Checks the server queue
    def checkQueue(self):
        for p in self.queue:
            if(len(self.clients)>=p["users"]):
                self.queue.remove(p)
                self.transfer(p)
    def start(self):
        print("================Server Starting==============")
        while True:
            pckt,address=self.socket.recvfrom(4096)
            msg=pickle.loads(pckt)
            #for clients initializing their app
            if(msg.flag=="INIT"):
                self.clients.append(address)
                print("Hello ",address[0],":",address[1])
                self.greetUser(address)
                self.checkQueue()
            #For fiel transfer request
            #TODO: finish the transfer method
            elif(msg.flag=="RQ"):
                print(address[0],":",address[1]," MSG: ",msg.data)
                self.queue.append(msg.data)
                self.checkQueue()
            #For clients closinf their application
            elif(msg.flag=="BYE"):
                print("Bye ",address[0],":",address[1])
                self.clients.remove(address)
            #To see weird packets
            else:
                print(address[0],":",address[1]," MSG: ",msg.data)
            self.updateUsers()
            
    

if __name__=="__main__":
    host=input("Host: ")        
    port=int(input("Port: "))
    server=Server(host,port)
    server.start()