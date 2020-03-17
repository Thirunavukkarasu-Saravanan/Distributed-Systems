"""
-------------------------------------------------------------------------
Name : Saravanan Thirunavukkarasu                                        |
-------------------------------------------------------------------------
"""

import socket
import sys
import time
import tkinter as tk
from _thread import *
from random import randint
import datetime
import queue

# import requests

isAlive = True
isContinue = True
conenctedClient = {};
dataQueue = queue.Queue()
isQueueAlive = False
connectionProcess = {}
gCounter = 0



#Write to GUI
def write(string):
    text_box.config(state=tk.NORMAL)
    text_box.insert("end", string + "\n")
    text_box.see("end")
    text_box.config(state=tk.DISABLED)

class ReceivedData:
    ''' STANDARD USER DATA TYPE TO HANDLE ALL THE DATA IN QUEUE  '''
    def __init__(self,c,a,p,d):
        self.connection = c;
        self.address = a;
        print(p)
        self.clientPID = p;        
        print("connectionasdasd")
        self.codedData = d;
       
        
        self.decodedData = d.decode("ascii");
        print("connection")
        self.timeStamp = datetime.datetime.now();
     
    def GetData(self,isCoded = False):
        if (isCoded):
            return self.codedData
        else:
            return self.decodedData
    #Timestamp data value 
    def GetCreatedTime(self):
        return self.timeStamp
    #Process ID
    def GetPID(self):
        return self.clientPID;
    #Connection Establish
    def GetConnection(self):
        return self.connection;
    #Address
    def GetAddress(self):
        return self.address
    #Timestamp 
    def GetTimeStamp(self):
        return self.timeStamp;
    #To calculate the wait time 
    def CalcualteWaitTime(self):
        t1 = self.timeStamp
        t2 = datetime.datetime.now()
        diff = (t2-t1).total_seconds()
        return diff


#Function for terminating connection.

def stop_conn():
    write("Stop")
    global isAlive, isContinue,isQueueAlive
    isContinue = False
    isAlive = False
    isQueueAlive = False

#Function for establishing connection.
    
def start_conn():
    print("Server")
    my_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = '127.0.0.1'
    port = 9998
    print(host)
    write(host)
    #Binding address to socket
    my_server.bind((host, port))
    #Setting socket to Non-block mode 
    my_server.setblocking(0)
    #Wait and listen for Client connection 
    my_server.listen(5)
    #Implementing a time frame for accepting connections
    my_server.settimeout(10)
    write("Server ")
    write("LISTENING...")
    count = 0
    c = None
    global isAlive, dataQueue,isQueueAlive,conenctedClient
    isAlive = True
    isQueueAlive = True
    start_new_thread(HandlePrcess,())
    while isAlive:
        c = None
        address = None
        try:
            c, address = my_server.accept()
            count = count + 1
            print("server check connected from " + str(address))
            tempRemoteID = str(address[0])+":"+ str(address[1])
            conenctedClient[tempRemoteID] = True       
            start_new_thread(connection_thread, (c, address))
        except:
            print("error in start_con fn: ", sys.exc_info()[0])
            if c is not None:
                c.close()
            isAlive = False
    if c is not None:
        c.close()



def connection_thread(c, ad):
    try:
        global isContinue,isQueueAlive,connectionProcess
        isContinue = True
        isShowMsg = True
        while isContinue:
            data = c.recv(1024)
            deocded_data = data.decode("ascii")
            #Random time to wait recieved from client
            ttt = str(deocded_data.split(",")[0])
            #Process ID of client 
            client_pid = str(deocded_data.split(",")[1])
            if (isShowMsg):
                print("\n New conection created with client ID "+ client_pid+ "(Remote Address :" + str(ad[0])+":"+str(ad[1]) + ")\n")
                write("\n New conection created with client ID "+ client_pid+ "(Remote Address :" + str(ad[0])+":"+str(ad[1]) + ")\n")
                isShowMsg = False
            qData = (c,ad,client_pid,data,datetime.datetime.now())
            #Queue the data
            dataQueue.put(qData)
            isQueueAlive = True
            tmpRemoteID = str(ad[0])+":"+ str(ad[1])
            connectionProcess[tmpRemoteID] = True
            while (connectionProcess.get(tmpRemoteID)):
                pass
            else:
                time.sleep(1)
            isContinue = True
        c.close()
    except:
        print("error in connection_thread fn: ", sys.exc_info()[0])
        c.close()



def CalculateTimeDifference(t1):
    t2 = datetime.datetime.now()
    diff = (t2-t1).total_seconds()
    return diff

def HandlePrcess():
    global isQueueAlive,dataQueue,gCounter
    while (isQueueAlive):
        while (not dataQueue.empty()):
            try:
                # Get the data from Queue
                rData = dataQueue.get()
                # Reassiging the variables
                clientConnection = rData[0]
                clientAddress = rData[1]
                clientPID = rData[2]
                clientData = rData[3]
                clientTimeStamp = rData[4]
                # Creating a Temporary remote address
                rmtAddress = str(clientAddress[0]) +":"+ str(clientAddress[1])
                # Reassigning the client Data (Decoded Data)
                cData = clientData.decode("ascii")
                #Random time sent by the client to wait 
                tttServer = str(cData.split(",")[0])
                #Client's Process ID
                cPID = str(cData.split(",")[1])
                # Making the thread to sleep for the random time sent by the client 
                time.sleep(int(tttServer))
                # Calculating the total time waited by the client
                tttClient = str(CalculateTimeDifference(clientTimeStamp))
                # Actual message that will be sent to the client to console
                ActualMsg = ""
                ActualMsg += "\n Server waited  " + tttServer + " seconds for Client " + cPID + "."
                ActualMsg += "\n Total time Client " + "(" + cPID + ")" +  " waited : " + tttClient + " seconds for the server response" + "."
                print("\n--------------------\n");
                print(ActualMsg)
                print("\n--------------------\n");
                # Message to be sent to the client in HTML Format (used in broswer)
                MsgToClient = ""
                MsgToClient += "<html>"
                MsgToClient += "<body>"
                #MsgToClient += "<h1>Response from Server</h1>"
                MsgToClient += "<h1>Server waited  " + tttServer + " seconds for Client " + cPID +  "." + "</h1>"
                MsgToClient += "<p> Total time Client " + "(" + cPID + ")" + " waited : " + tttClient + " seconds for the server response " +  "." + "</p>"
                MsgToClient += "</body>"
                MsgToClient += "</html>"
                # Message to be logged in server
                ServerMsg = ""
                ServerMsg += "\n Request Method  : POST"
                ServerMsg += "\n Status Code     : 200"
                ServerMsg += "\n Remote Address  : " + rmtAddress
                ServerMsg += "\n Date            : " + str(datetime.datetime.now())
                ServerMsg += "\n Status          : HTTP/1.0 200 OK"
                ServerMsg += "\n Content-length  : " + str(len(MsgToClient))
                ServerMsg += "\n Content-type    : text/html"
                ServerMsg += "\n" + MsgToClient + "\n" 
                #Send the data to the respective client
                write(ServerMsg)
                clientConnection.send(ActualMsg.encode("ascii"))
                print(ServerMsg)
                connectionProcess[rmtAddress] = False
                gCounter += 1
                print("\n Data Queue " + str(gCounter) + " has finished\n")
            except:
                print("error in handle fn: ", sys.exc_info()[0])
                print("error in handle fn\n\n\n")
    isQueueAlive = False
        




# Tkinter initizalation
root = tk.Tk()
# Frame
frame = tk.Frame(root)
frame.pack()
#Textbox
text_box = tk.Text(root, state=tk.DISABLED)
text_box.pack()
# Window Attributes
mainWin = root
mainWin.title = "Server"
mainWin.geometry("300x480")
# Stop Button
button1 = tk.Button(frame, text="QUIT", fg="red", command=stop_conn)
button1.pack(side=tk.RIGHT)
# Start Button
button2 = tk.Button(frame, text="CONNECT", fg="green", command=start_conn)
button2.pack(side=tk.RIGHT)
# Tkinter Start
root.mainloop()


