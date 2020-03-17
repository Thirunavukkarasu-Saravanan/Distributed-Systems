"""
--------------------------------------------------------------------------
Name : Saravanan Thirunavukkarasu                                        |
------------------------------------------------------------------------
"""

import socket
import sys
import time
import tkinter as tk
from _thread import *
from random import randint

# import requests

isAlive = True
isContinue = True
connection = {}

#Function for terminating connection.

def stop_conn():
    print("Stop")
    global connection, isAlive, isContinue
    isContinue = False
    isAlive = False
    #connection.close()

#Function for establishing connection.
    
def start_conn():
    print("Server")
    my_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = '127.0.0.1'
    port = 9998
    print(host)
    #Binding address to socket
    my_server.bind((host, port))
    #Setting socket to Non-block mode 
    my_server.setblocking(0)
    #Wait and listen for Client connection 
    my_server.listen(5)
    #Implementing a time frame for accepting connections
    my_server.settimeout(30)
    print("LISTENING...")
    count = 0
    c = None
    global isAlive, connection
    isAlive = True

    while isAlive:
        c = None
        address = None
        try:
            c, address = my_server.accept()
            connection = c
            count = count + 1
            print("server check connected from %s" % str(address))
            start_new_thread(connection_thread, (c, address))
            print(c)
        except:
            print("error : ", sys.exc_info()[0])
            if c is not None:
                c.close()
            isAlive = False
    if c is not None:
        c.close()


def connection_thread(c, ad):
    try:
        global isContinue
        isContinue = True
        while isContinue:
            data = c.recv(1024)
            deocded_data = data.decode("ascii")
            #Random time to wait recieved from client
            ttt = str(deocded_data.split(",")[0])
            #Process ID of client 
            client_pid = str(deocded_data.split(",")[1])
            #print(client_pid)
            print("Random Time to Wait sent from client with process Id  " + client_pid + " is " + ttt)
            time.sleep(int(ttt))
            if not data:
                break
            msg = 'The Server waited for ' + ttt + "."
            print("Message sent to port " + str(ad[1]) + " is : '" + msg + "'")
            c.send(msg.encode('ascii'))
            isContinue = True
        c.close()
    except:
        print("error : ", sys.exc_info()[0])
        c.close()





# Tkinter initizalation
root = tk.Tk()
# Frame
frame = tk.Frame(root)
frame.pack()
# Window Attributes
mainWin = root
mainWin.title = "Server"
mainWin.geometry("300x480")
# Stop Button
button1 = tk.Button(frame, text="QUIT", fg="red", command=stop_conn)
button1.pack(side=tk.LEFT)
# Start Button
button2 = tk.Button(frame, text="CONNECT", fg="green", command=start_conn)
button2.pack(side=tk.LEFT)
# Tkinter Start
root.mainloop()
