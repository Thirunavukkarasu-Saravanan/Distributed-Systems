"""
--------------------------------------------------------------------------
Name : Saravanan Thirunavukkarasu                                        |
--------------------------------------------------------------------------
"""



import socket
import sys
import tkinter as tk
from _thread import *
from random import randint
import os
import time

# import requests

conn = None
isContinue = False
pid = os.getpid()



#Write to GUI
def write(string):
    text_box.config(state=tk.NORMAL)
    text_box.insert("end", string + "\n")
    text_box.see("end")
    text_box.config(state=tk.DISABLED)


#Function for terminating connection

def stop_conn():
    """Function for stop button"""
    write("Stop")
    global conn, isContinue
    #conn.close()
    isContinue = False

#Function for establishing connection
    
def start_conn():
    """Function for start button"""
    write("Start")
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
            rand = (randint(3, 10))
            request = str(rand) + "," + str(pid)
            
            entity = "Random number sent is :" +  str(rand)
            entity2 = len(entity)
            localtime = time.asctime( time.localtime(time.time()) )
            tempStr = "GET + Host : 127.0.0.1 + User-Agent : Mozilla/5.0 (Windows 10.0; Win64; x64; rv:47:0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36   + Random number sent is : "+ str(rand) +  " + Content-Length :"+ str(entity2) + " Date :"+ str(localtime)
            write(tempStr)
            client.send(str(request).encode("ascii"))
            msg = client.recv(1024)
            write("\n")
            write(msg.decode('ascii'))
            write("\n")
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

#Textbox
text_box = tk.Text(root, state=tk.DISABLED)
text_box.pack()

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
