"""
--------------------------------------------------------------------------
Name : Saravanan Thirunavukkarasu                                        |
--------------------------------------------------------------------------
"""



import socket
import sys
import tkinter as tk
from _thread import *
#from datetime import *
from random import randint
import os

# import requests

conn = None
isContinue = False
pid = os.getpid()

#Function for terminating connection

def stop_conn():
    """Function for stop button"""
    print("Stop")
    global conn, isContinue
    # conn.close()
    isContinue = False

#Function for establishing connection
    
def start_conn():
    """Function for start button"""
    print("Start")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 9998
    client.connect((host, port))
    global isContinue
    isContinue = True
    global conn
    conn = client
    start_new_thread(connected_thread, (client,))



 
def connected_thread(client):
    """Function for Thread"""
    global isContinue
    try:
        while isContinue:
            rand = (randint(1, 5))
            request = str(rand) + "," + str(pid)
            print("Random number sent is : ", str(rand))
            client.send(str(request).encode("ascii"))
            msg = client.recv(1024)
            print(msg.decode('ascii'))
            print("\n")
        client.close()
        print("Connection Terminated,,,,")
    except:
        print("error : ", sys.exc_info()[0])
        print("Error.. Connection Closed.")




# Tkinter initizalation
root = tk.Tk()

# Frame
frame = tk.Frame(root)
frame.pack()

# Window Attributes
mainWin = root
mainWin.title = "Client"
mainWin.geometry("300x480")

# Stop Button
but1 = tk.Button(frame, text="STOP", fg="red", command=stop_conn)
but1.pack(side=tk.RIGHT)

# Communicate Button
but2 = tk.Button(frame, text='COMMUNICATE', fg="blue", command=start_conn)
but2.pack(side=tk.RIGHT)

# Tkinter Start
root.mainloop()
